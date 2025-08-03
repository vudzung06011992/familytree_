from flask import Flask, jsonify, request
import pandas as pd
import json
from collections import defaultdict
from flask_cors import CORS  # Cho phép gọi từ HTML JS

app = Flask(__name__)
CORS(app)  # Bật CORS để cho phép gọi từ browser
import os 

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Lưu file upload
    file.save('Thong tin gia dinh.xlsm')
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/api/family", methods=["GET"])
def get_family_data():

    file_path = os.path.join(os.path.dirname(__file__), 'Thong tin gia dinh.xlsm')
    # Đọc sheet 'Data' và 'Relationship'
    df_data = pd.read_excel(file_path, sheet_name='Data', engine='openpyxl')
    df_rels = pd.read_excel(file_path, sheet_name='Relationship', engine='openpyxl')

    # Khởi tạo dict lưu quan hệ
    rels_dict = defaultdict(lambda: defaultdict(list))

    # ROLE ID mapping
    SPOUSE_ROLES = {1, 2}           # Vợ, Chồng
    FATHER_ROLE = {3, 7, 15}                # Bố ruột
    MOTHER_ROLE = {4, 8, 16}                 # Mẹ ruột
    CHILD_ROLES = {5, 6, 9, 10, 17}            # Con trai ruột, con gái ruột

    # Xử lý quan hệ
    for _, row in df_rels.iterrows():
        id1 = str(row["entity_id_1"])
        id2 = str(row["entity_id_2"])
        rel_type = row["connection_type_id"]
        role1 = int(row["entity_id_1_role_id"])
        role2 = int(row["entity_id_2_role_id"])

        # Vợ - chồng (2 chiều)
        if rel_type == 1 and role1 in SPOUSE_ROLES and role2 in SPOUSE_ROLES:
            rels_dict[id1]["spouses"].append(id2)
            rels_dict[id2]["spouses"].append(id1)

        # Bố mẹ - con
        elif rel_type == 2:
            if role1 in FATHER_ROLE and role2 in CHILD_ROLES:
                if "father" not in rels_dict[id2]:
                    rels_dict[id2]["father"] = id1
                rels_dict[id1]["children"].append(id2)

            elif role1 in MOTHER_ROLE and role2 in CHILD_ROLES:
                if "mother" not in rels_dict[id2]:
                    rels_dict[id2]["mother"] = id1
                rels_dict[id1]["children"].append(id2)

            elif role1 in CHILD_ROLES and role2 in FATHER_ROLE:
                if "father" not in rels_dict[id1]:
                    rels_dict[id1]["father"] = id2
                rels_dict[id2]["children"].append(id1)

            elif role2 in MOTHER_ROLE and role1 in CHILD_ROLES:
                if "mother" not in rels_dict[id1]:
                    rels_dict[id1]["mother"] = id2
                rels_dict[id2]["children"].append(id1)

            else:
                return jsonify({"error": "Invalid relationship roles for relationship of id1: {}, id2: {}".format(id1, id2)}), 400

    # Hàm bổ sung quan hệ đối xứng
    def add_symmetric_relationships(rels_dict, df_data):
        """
        Bổ sung các quan hệ đối xứng thiếu:
        - Vợ chồng: nếu A có spouse B mà B không có spouse A
        - Bố con: nếu A có father B mà B không có children A
        - Mẹ con: nếu A có mother B mà B không có children A
        """
        # Tạo mapping giới tính
        gender_map = {}
        for _, row in df_data.iterrows():
            person_id = str(row["entity_id"])
            gender_raw = str(row.get("gender", "")).strip()
            
            # Chuyển đổi giới tính về M/F
            if gender_raw.upper() in ["NAM", "MALE", "M"]:
                gender = "M"
            elif gender_raw.upper() in ["NỮ", "NU", "FEMALE", "F"]:
                gender = "F"
            else:
                gender = gender_raw.upper()  # Giữ nguyên nếu không match
                
            gender_map[person_id] = gender
        
        # Lấy tất cả các ID người
        all_ids = set(rels_dict.keys())
        
        # Duyệt qua từng người
        for person_id in list(all_ids):
            rels = rels_dict[person_id]
            
            # Xử lý quan hệ vợ chồng
            if "spouses" in rels:
                for spouse_id in rels["spouses"]:
                    # Đảm bảo spouse_id tồn tại trong rels_dict
                    if spouse_id not in rels_dict:
                        rels_dict[spouse_id] = defaultdict(list)
                    
                    # Nếu spouse không có quan hệ ngược lại, thêm vào
                    if "spouses" not in rels_dict[spouse_id]:
                        rels_dict[spouse_id]["spouses"] = []
                    if person_id not in rels_dict[spouse_id]["spouses"]:
                        rels_dict[spouse_id]["spouses"].append(person_id)
            
            # Xử lý quan hệ bố con
            if "father" in rels:
                father_id = rels["father"]
                # Đảm bảo father_id tồn tại trong rels_dict
                if father_id not in rels_dict:
                    rels_dict[father_id] = defaultdict(list)
                
                # Nếu bố không có con này, thêm vào
                if "children" not in rels_dict[father_id]:
                    rels_dict[father_id]["children"] = []
                if person_id not in rels_dict[father_id]["children"]:
                    rels_dict[father_id]["children"].append(person_id)
            
            # Xử lý quan hệ mẹ con
            if "mother" in rels:
                mother_id = rels["mother"]
                # Đảm bảo mother_id tồn tại trong rels_dict
                if mother_id not in rels_dict:
                    rels_dict[mother_id] = defaultdict(list)
                
                # Nếu mẹ không có con này, thêm vào
                if "children" not in rels_dict[mother_id]:
                    rels_dict[mother_id]["children"] = []
                if person_id not in rels_dict[mother_id]["children"]:
                    rels_dict[mother_id]["children"].append(person_id)
            
            # Xử lý quan hệ con - cha/mẹ (ngược lại)
            if "children" in rels:
                for child_id in rels["children"]:
                    # Đảm bảo child_id tồn tại trong rels_dict
                    if child_id not in rels_dict:
                        rels_dict[child_id] = defaultdict(list)
                    
                    # Xác định giới tính để biết là father hay mother
                    parent_gender = gender_map.get(person_id, "")
                    
                    if parent_gender in ["M", "MALE", "NAM"]:
                        # Đây là bố
                        if "father" not in rels_dict[child_id]:
                            rels_dict[child_id]["father"] = person_id
                    elif parent_gender in ["F", "FEMALE", "NỮ"]:
                        # Đây là mẹ  
                        if "mother" not in rels_dict[child_id]:
                            rels_dict[child_id]["mother"] = person_id
    
    # Bổ sung quan hệ đối xứng
    print("🔄 Đang bổ sung các quan hệ đối xứng...")
    original_count = sum(len(rels) for rels in rels_dict.values())
    add_symmetric_relationships(rels_dict, df_data)
    final_count = sum(len(rels) for rels in rels_dict.values())
    print(f"✅ Đã bổ sung {final_count - original_count} quan hệ đối xứng")

    # Hàm xử lý boolean
    def to_bool(val):
        return bool(val) if pd.notna(val) else False

    # Hàm chuyển đổi giới tính
    def convert_gender(gender_raw):
        gender_str = str(gender_raw).strip()
        if gender_str.upper() in ["NAM", "MALE", "M"]:
            return "M"
        elif gender_str.upper() in ["NỮ", "NU", "FEMALE", "F"]:
            return "F"
        else:
            return gender_str  # Giữ nguyên nếu không match

    # Xây dựng list người
    people = []
    for _, row in df_data.iterrows():
        pid = str(row["entity_id"])
        person = {
            "id": pid,
            "rels": rels_dict.get(pid, {}),
            "data": {
                "first name": row.get("first_name", " "),
                "middle name": row.get("middle_name", " "),
                "last name": row.get("last_name", " "),
                "alias": row.get("alias", " "),
                "gender": convert_gender(row.get("gender", " ")),
                "birthday": pd.to_datetime(row.get("date_of_birth", " "), errors="coerce").strftime("%Y") if pd.notna(row.get("date_of_birth", " ")) else " ",

                "avatar": " ",
                "nationality": row.get("nationality", " "),
                "place of origin": row.get("place_of_origin", " "),
                "place of birth": row.get("place_of_birth", " "),
                "place of residence": row.get("place_of_residence", " "),
                "is dead": to_bool(row.get("is_dead", 0)),
                "date of death": pd.to_datetime(row.get("date_of_death", " "), errors="coerce").strftime("%Y-%m-%d") if pd.notna(row.get("date_of_death", " ")) else " ",

                "place of death": row.get("place_of_death", " "),
                "ethnicity": row.get("ethnicity", " "),
                "educational level": row.get("educational_level", " "),
                "is cpv member": to_bool(row.get("is_cpv_member", 0)),
                "occupation": row.get("occupation", " "),
                "career": row.get("career", " "),
                "characteristics": row.get("characteristics", " "),
                "phone": row.get("phone", " "),
                "email": row.get("email", " "),
                "full name": row.get("full_name", " "),
                "last update": pd.to_datetime(row.get("last_update_date", " "), errors="coerce").strftime("%Y-%m-%d %H:%M:%S") if pd.notna(row.get("last_update_date", " ")) else " "
            }
        }
        people.append(person)

    # Hàm thay NaN/None bằng chuỗi rỗng " "
    def clean_nans(obj):
        if isinstance(obj, dict):
            return {k: clean_nans(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [clean_nans(i) for i in obj]
        elif pd.isna(obj):
            return " "
        else:
            return obj

    # Làm sạch dữ liệu
    people_cleaned = clean_nans(people)

    # Ghi ra file
    with open("family_people_list.json", "w", encoding="utf-8") as f:
        json.dump(people_cleaned, f, indent=2, ensure_ascii=False)
    print(people_cleaned)
    print("✅ Đã tạo xong file family_people_list.json với NaN → ' '")

    return jsonify(people_cleaned)

if __name__ == "__main__":
    app.run(debug=True)
