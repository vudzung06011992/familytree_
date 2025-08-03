from flask import Flask, jsonify, request, make_response
import pandas as pd
import json
from collections import defaultdict
from flask_cors import CORS  # Cho phép gọi từ HTML JS
import tkinter as tk
from tkinter import messagebox
import sys

app = Flask(__name__)
# Cấu hình CORS - cho phép tất cả origins cho development
CORS(app, 
     origins="*",  # Allow all origins for development
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
import os 

def add_cors_headers(response):
    """Thêm CORS headers manually"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.after_request
def after_request(response):
    """Thêm CORS headers cho tất cả responses"""
    return add_cors_headers(response) 

def show_error_and_stop(error_message):
    """
    Hiển thị lỗi chi tiết trong popup window
    """
    print(f"❌ CRITICAL ERROR: {error_message}")
    
    # Tạo popup window với thông tin chi tiết hơn
    try:
        root = tk.Tk()
        root.withdraw()  # Ẩn main window
        root.attributes('-topmost', True)  # Luôn hiện trên top
        
        # Tạo title và message chi tiết
        title = "Family Tree Server - Lỗi Dữ Liệu"
        detailed_message = f"""
❌ PHÁT HIỆN LỖI TRONG DỮ LIỆU EXCEL:

{error_message}

⚠️ LƯU Ý: Server vẫn đang chạy, có thể upload lại sau khi sửa.
        """
        
        messagebox.showerror(title, detailed_message)
        root.destroy()
        
    except Exception as e:
        print(f"❌ Không thể hiện popup: {e}")
        print(f"📋 CHI TIẾT LỖI: {error_message}")
    
    return True  # Indicate error occurred

def show_biological_parent_error(child_id, parent_type, existing_parent_id, new_parent_id):
    """
    Hiển thị lỗi cụ thể cho biological parent conflicts
    """
    parent_name = "bố ruột" if parent_type == "father" else "mẹ ruột"
    error_message = f"""
⚠️ XUNG ĐỘT QUAN HỆ {parent_name.upper()}:
Người con ID {child_id} có 2 {parent_name}: ID {existing_parent_id} và ID {new_parent_id}

🛠 CÁCH SỬA:
1. Mở sheet 'Relationship' trong Excel
2. Sửa/Xóa dòng xung đột
    """
    
    show_error_and_stop(error_message)
import sys

app = Flask(__name__)
CORS(app, origins=["http://localhost:8000", "http://127.0.0.1:8000"])  # Cho phép cả localhost và 127.0.0.1
import os 

def show_error_and_stop(error_message):
    """
    Hiển thị lỗi chi tiết trong popup window
    """
    print(f"❌ CRITICAL ERROR: {error_message}")
    
    # Tạo popup window với thông tin chi tiết hơn
    try:
        root = tk.Tk()
        root.withdraw()  # Ẩn main window
        root.attributes('-topmost', True)  # Luôn hiện trên top
        
        # Tạo title và message chi tiết
        title = "Family Tree Server - Lỗi Dữ Liệu"
        detailed_message = f"""
❌ PHÁT HIỆN LỖI TRONG DỮ LIỆU EXCEL:

{error_message}

⚠️ LƯU Ý: Server vẫn đang chạy, có thể upload lại sau khi sửa.
        """
        
        messagebox.showerror(title, detailed_message)
        root.destroy()
        
    except Exception as e:
        print(f"❌ Không thể hiện popup: {e}")
        print(f"📋 CHI TIẾT LỖI: {error_message}")
    
    return True  # Indicate error occurred

def show_biological_parent_error(child_id, parent_type, existing_parent_id, new_parent_id):
    """
    Hiển thị lỗi cụ thể cho biological parent conflicts
    """
    parent_name = "bố ruột" if parent_type == "father" else "mẹ ruột"
    role_id = "3" if parent_type == "father" else "4"
    error_message = f"""
⚠️ XUNG ĐỘT QUAN HỆ {parent_name.upper()}:
Người con ID {child_id} có 2 {parent_name}: ID {existing_parent_id} và ID {new_parent_id}

� CÁCH SỬA:
1. Mở sheet 'Relationship' trong Excel
2. Tìm dòng mô tả quan hệ giữa (i) ID {child_id} và ID {existing_parent_id}; (i) ID {child_id} và ID {new_parent_id}; 
3. Quyết định:
   • Sửa role_id 
   • Hoặc xóa dòng xung đột
    """
    
    show_error_and_stop(error_message) 

def write_output_file(data, is_error=False):
    """
    Hàm helper để ghi file JSON output
    - Nếu is_error=True: ghi file với format error
    - Nếu is_error=False: ghi file với dữ liệu bình thường
    """
    filename = "family_people_list.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Đã ghi file {filename}")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi ghi file {filename}: {str(e)}")
        return False

@app.route("/upload", methods=["POST", "OPTIONS"])
def upload_file():
    # Handle preflight requests
    if request.method == "OPTIONS":
        response = make_response()
        return add_cors_headers(response)
        
    if 'file' not in request.files:
        error_data = {"error": "No file provided"}
        write_output_file(error_data, is_error=True)
        response = make_response(jsonify(error_data))
        return add_cors_headers(response)
    
    file = request.files['file']
    if file.filename == '':
        error_data = {"error": "No file selected"}
        write_output_file(error_data, is_error=True)
        response = make_response(jsonify(error_data))
        return add_cors_headers(response)
    
    # Lưu file upload
    file.save('Thong tin gia dinh.xlsm')
    response = make_response(jsonify({"message": "File uploaded successfully"}), 200)
    return add_cors_headers(response)

@app.route("/api/family", methods=["GET", "OPTIONS"])
def get_family_data():
    # Handle preflight requests
    if request.method == "OPTIONS":
        response = make_response()
        return add_cors_headers(response)
        
    file_path = os.path.join(os.path.dirname(__file__), 'Thong tin gia dinh.xlsm')
    print(f"📁 Reading file: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        show_error_and_stop(f"File not found: {file_path}")
        return jsonify({"error": f"File not found: {file_path}"})
    
    # Đọc sheet 'Data' và 'Relationship'
    try:
        df_data = pd.read_excel(file_path, sheet_name='Data', engine='openpyxl')
        df_rels = pd.read_excel(file_path, sheet_name='Relationship', engine='openpyxl')
    except Exception as e:
        print(f"❌ Error reading Excel: {str(e)}")
        show_error_and_stop(f"Error reading Excel: {str(e)}")
        return jsonify({"error": f"Error reading Excel: {str(e)}"})
    
    print(f"📊 Data sheet: {len(df_data)} rows")
    print(f"🔗 Relationship sheet: {len(df_rels)} rows")

    # Khởi tạo dict lưu quan hệ
    rels_dict = defaultdict(lambda: defaultdict(list))

    # ROLE ID mapping theo bảng role_id
    SPOUSE_ROLES = {1, 2}                    # Vợ, Chồng
    BIOLOGICAL_FATHER_ROLE = {3}             # Bố ruột (chỉ dành cho father field)
    BIOLOGICAL_MOTHER_ROLE = {4}             # Mẹ ruột (chỉ dành cho mother field)
    BIOLOGICAL_CHILD_ROLES = {5, 6}          # Con trai ruột, Con gái ruột (chỉ dành cho father/mother field)
    
    # Tất cả loại cha - dành cho children field
    ALL_FATHER_ROLES = {3, 7, 15}            # Bố ruột, Bố nuôi, Cha dượng
    # Tất cả loại mẹ - dành cho children field  
    ALL_MOTHER_ROLES = {4, 8, 16}            # Mẹ ruột, Mẹ nuôi, Mẹ kế
    # Tất cả loại con - dành cho children field
    ALL_CHILD_ROLES = {5, 6, 9, 10, 17}      # Con ruột, Con nuôi, Con riêng

    # Xử lý quan hệ
    for idx, row in df_rels.iterrows():
        id1 = str(row["entity_id_1"])
        id2 = str(row["entity_id_2"])
        rel_type = row["connection_type_id"]
        role1 = int(row["entity_id_1_role_id"])
        role2 = int(row["entity_id_2_role_id"])
        
        print(f"🔗 Processing relationship {idx}: {id1}({role1}) -> {id2}({role2}), type={rel_type}")

        # Vợ - chồng (2 chiều)
        if rel_type == 1 and role1 in SPOUSE_ROLES and role2 in SPOUSE_ROLES:
            if id2 not in rels_dict[id1]["spouses"]:
                rels_dict[id1]["spouses"].append(id2)
            if id1 not in rels_dict[id2]["spouses"]:
                rels_dict[id2]["spouses"].append(id1)

        # Bố mẹ - con
        elif rel_type == 2:
            # Xử lý tất cả các loại quan hệ parent-child cho children field
            if (role1 in ALL_FATHER_ROLES or role1 in ALL_MOTHER_ROLES) and role2 in ALL_CHILD_ROLES:
                # Parent -> Child: thêm vào children
                if id2 not in rels_dict[id1]["children"]:
                    rels_dict[id1]["children"].append(id2)
                
                # CHỈ set father/mother field cho quan hệ RUỘT
                if role1 in BIOLOGICAL_FATHER_ROLE and role2 in BIOLOGICAL_CHILD_ROLES:
                    if "father" in rels_dict[id2] and rels_dict[id2]["father"] != id1:
                        existing_father = rels_dict[id2]["father"]
                        show_biological_parent_error(id2, "father", existing_father, id1)
                        error_msg = "Child {} already has a biological father (ID {}). Cannot assign multiple fathers. New conflicting father: ID {}".format(id2, existing_father, id1)
                        return jsonify({"error": error_msg})
                    rels_dict[id2]["father"] = id1

                elif role1 in BIOLOGICAL_MOTHER_ROLE and role2 in BIOLOGICAL_CHILD_ROLES:
                    if "mother" in rels_dict[id2] and rels_dict[id2]["mother"] != id1:
                        existing_mother = rels_dict[id2]["mother"]
                        show_biological_parent_error(id2, "mother", existing_mother, id1)
                        error_msg = "Child {} already has a biological mother (ID {}). Cannot assign multiple mothers. New conflicting mother: ID {}".format(id2, existing_mother, id1)
                        return jsonify({"error": error_msg})
                    rels_dict[id2]["mother"] = id1

            elif role1 in ALL_CHILD_ROLES and (role2 in ALL_FATHER_ROLES or role2 in ALL_MOTHER_ROLES):
                # Child -> Parent: thêm vào children
                if id1 not in rels_dict[id2]["children"]:
                    rels_dict[id2]["children"].append(id1)
                
                # CHỈ set father/mother field cho quan hệ RUỘT
                if role1 in BIOLOGICAL_CHILD_ROLES and role2 in BIOLOGICAL_FATHER_ROLE:
                    if "father" in rels_dict[id1] and rels_dict[id1]["father"] != id2:
                        existing_father = rels_dict[id1]["father"]
                        show_biological_parent_error(id1, "father", existing_father, id2)
                        error_msg = "Child {} already has a biological father (ID {}). Cannot assign multiple fathers. New conflicting father: ID {}".format(id1, existing_father, id2)
                        return jsonify({"error": error_msg})
                    rels_dict[id1]["father"] = id2
                elif role1 in BIOLOGICAL_CHILD_ROLES and role2 in BIOLOGICAL_MOTHER_ROLE:
                    if "mother" in rels_dict[id1] and rels_dict[id1]["mother"] != id2:
                        existing_mother = rels_dict[id1]["mother"]
                        show_biological_parent_error(id1, "mother", existing_mother, id2)
                        error_msg = "Child {} already has a biological mother (ID {}). Cannot assign multiple mothers. New conflicting mother: ID {}".format(id1, existing_mother, id2)
                        return jsonify({"error": error_msg})
                    rels_dict[id1]["mother"] = id2

            else:
                print(f"❌ Quan hệ giữa 02 ID sau chưa chính xác: Invalid relationship: {id1}({role1}) -> {id2}({role2}), type={rel_type}")
                error_msg = "Quan hệ giữa 02 ID sau chưa chính xác: Invalid relationship roles for relationship of id1: {}, id2: {}, role1: {}, role2: {}, rel_type: {}".format(id1, id2, role1, role2, rel_type)
                show_error_and_stop(error_msg)
                return jsonify({"error": error_msg})

    # Hàm bổ sung quan hệ đối xứng theo logic mới
    def add_symmetric_relationships(rels_dict, df_data):
        """
        Bổ sung các quan hệ đối xứng cho biological relationships:
        - Nếu con có father/mother mà bố/mẹ không có con này trong children thì bổ sung
        - Chỉ áp dụng cho quan hệ ruột (biological)
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
                gender = gender_raw.upper()
                
            gender_map[person_id] = gender
        
        # Lấy tất cả các ID người
        all_ids = set(rels_dict.keys())
        
        # Duyệt qua từng người để bổ sung quan hệ đối xứng
        for person_id in list(all_ids):
            rels = rels_dict[person_id]
            
            # Xử lý quan hệ vợ chồng (giữ nguyên)
            if "spouses" in rels:
                for spouse_id in rels["spouses"]:
                    if spouse_id not in rels_dict:
                        rels_dict[spouse_id] = defaultdict(list)
                    
                    if "spouses" not in rels_dict[spouse_id]:
                        rels_dict[spouse_id]["spouses"] = []
                    if person_id not in rels_dict[spouse_id]["spouses"]:
                        rels_dict[spouse_id]["spouses"].append(person_id)
            
            # Bổ sung quan hệ bố-con: nếu con có father mà father không có con này
            if "father" in rels:
                father_id = rels["father"]
                if father_id not in rels_dict:
                    rels_dict[father_id] = defaultdict(list)
                
                if "children" not in rels_dict[father_id]:
                    rels_dict[father_id]["children"] = []
                if person_id not in rels_dict[father_id]["children"]:
                    rels_dict[father_id]["children"].append(person_id)
            
            # Bổ sung quan hệ mẹ-con: nếu con có mother mà mother không có con này
            if "mother" in rels:
                mother_id = rels["mother"]
                if mother_id not in rels_dict:
                    rels_dict[mother_id] = defaultdict(list)
                
                if "children" not in rels_dict[mother_id]:
                    rels_dict[mother_id]["children"] = []
                if person_id not in rels_dict[mother_id]["children"]:
                    rels_dict[mother_id]["children"].append(person_id)
            
            # Bổ sung quan hệ con-cha/mẹ: nếu bố/mẹ có con mà con không có father/mother (CHỈ cho quan hệ ruột)
            if "children" in rels:
                for child_id in rels["children"]:
                    if child_id not in rels_dict:
                        rels_dict[child_id] = defaultdict(list)
                    
                    # Xác định giới tính để biết là father hay mother
                    parent_gender = gender_map.get(person_id, "")
                    
                    if parent_gender in ["M", "MALE", "NAM"]:
                        # Đây là bố - chỉ set nếu con chưa có father
                        if "father" not in rels_dict[child_id]:
                            rels_dict[child_id]["father"] = person_id
                    elif parent_gender in ["F", "FEMALE", "NỮ"]:
                        # Đây là mẹ - chỉ set nếu con chưa có mother
                        if "mother" not in rels_dict[child_id]:
                            rels_dict[child_id]["mother"] = person_id
    
    # Bổ sung quan hệ đối xứng
    print("🔄 Đang bổ sung các quan hệ đối xứng...")
    original_count = sum(len(rels) for rels in rels_dict.values())
    add_symmetric_relationships(rels_dict, df_data)
    final_count = sum(len(rels) for rels in rels_dict.values())
    print(f"✅ Đã bổ sung {final_count - original_count} quan hệ đối xứng")

    # Đảm bảo tất cả arrays đều unique
    print("🔄 Đang loại bỏ duplicate values...")
    for person_id in rels_dict:
        if "spouses" in rels_dict[person_id]:
            rels_dict[person_id]["spouses"] = list(set(rels_dict[person_id]["spouses"]))
        if "children" in rels_dict[person_id]:
            rels_dict[person_id]["children"] = list(set(rels_dict[person_id]["children"]))
    print("✅ Đã loại bỏ duplicate values")

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
    print("🔄 Đang xây dựng list người...")
    people = []
    for idx, row in df_data.iterrows():
        try:
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
        except Exception as e:
            print(f"❌ Error processing person {idx}: {str(e)}")
            show_error_and_stop(f"Error processing person {idx}: {str(e)}")
    
    print(f"✅ Đã xây dựng list {len(people)} người")

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
    print("🔄 Đang làm sạch dữ liệu...")
    try:
        people_cleaned = clean_nans(people)
        print("✅ Đã làm sạch dữ liệu")
    except Exception as e:
        print(f"❌ Error cleaning data: {str(e)}")
        show_error_and_stop(f"Error cleaning data: {str(e)}")

    # Ghi ra file JSON cho dữ liệu thành công
    print("🔄 Đang ghi file JSON...")
    try:
        write_output_file(people_cleaned, is_error=False)
        print("✅ Đã ghi file JSON")
    except Exception as e:
        print(f"❌ Error writing JSON: {str(e)}")
        show_error_and_stop(f"Error writing JSON: {str(e)}")
    
    print("✅ Đã tạo xong file family_people_list.json với NaN → ' '")

    print("🔄 Đang return JSON response...")
    try:
        response = make_response(jsonify(people_cleaned))
        return add_cors_headers(response)
    except Exception as e:
        print(f"❌ Error creating JSON response: {str(e)}")
        show_error_and_stop(f"Error creating JSON response: {str(e)}")
        error_response = make_response(jsonify({"error": str(e)}))
        return add_cors_headers(error_response)

if __name__ == "__main__":
    # Sử dụng port từ environment variable cho production, fallback về 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
