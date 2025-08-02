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
    FATHER_ROLE = 3                 # Bố ruột
    MOTHER_ROLE = 4                 # Mẹ ruột
    CHILD_ROLES = {5, 6}            # Con trai ruột, con gái ruột

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

        # Bố mẹ ruột - con ruột
        elif rel_type == 2:
            if role1 == FATHER_ROLE:
                if "father" not in rels_dict[id2]:
                    rels_dict[id2]["father"] = id1
                rels_dict[id1]["children"].append(id2)

            elif role1 == MOTHER_ROLE:
                if "mother" not in rels_dict[id2]:
                    rels_dict[id2]["mother"] = id1
                rels_dict[id1]["children"].append(id2)

            elif role1 in CHILD_ROLES:
                if role2 == FATHER_ROLE:
                    if "father" not in rels_dict[id1]:
                        rels_dict[id1]["father"] = id2
                    rels_dict[id2]["children"].append(id1)

                elif role2 == MOTHER_ROLE:
                    if "mother" not in rels_dict[id1]:
                        rels_dict[id1]["mother"] = id2
                    rels_dict[id2]["children"].append(id1)

    # Hàm xử lý boolean
    def to_bool(val):
        return bool(val) if pd.notna(val) else False

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
                "gender": row.get("gender", " "),
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
