from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 업로드 폴더가 없으면 생성
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 더미 케이스 데이터를 저장할 리스트
dummy_cases = []

@app.route('/api/cases', methods=['POST'])
def create_case():
    # 폼 데이터 가져오기
    case_name = request.form.get('caseName')
    description = request.form.get('description')
    incident_types = request.form.getlist('incidentTypes')
    
    # 업로드된 파일 처리
    uploaded_files = request.files.getlist('uploadFiles')
    file_count = len(uploaded_files)
    total_file_size = 0  # 바이트 단위
    saved_filenames = []
    
    for file in uploaded_files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_filenames.append(filename)
            total_file_size += os.path.getsize(file_path)
    
    # 총 파일 크기를 MB 단위로 변환 (소수점 둘째자리까지)
    total_file_size_mb = round(total_file_size / (1024 * 1024), 2)
    
    # 새 케이스 객체 생성 (분석 PC 수와 총 파일 크기는 업로드한 파일 수 및 크기로 결정)
    new_case = {
        "id": dummy_cases[-1]["id"] + 1 if dummy_cases else 1,
        "title": case_name,
        "description": description,
        "pcCount": file_count,                 # 업로드한 파일의 개수가 분석 PC 수
        "totalFileSize": total_file_size_mb,     # 업로드 파일의 총 크기 (MB)
        "incidentTypes": incident_types,
        "uploadedFiles": saved_filenames,
        "created_at": "2025-02-19T13:00:00"      # 예시 날짜
    }
    
    dummy_cases.append(new_case)
    return jsonify(new_case), 201

# GET 메서드: 모든 케이스 데이터를 JSON으로 반환
@app.route("/api/cases", methods=["GET"])
def get_cases():
    return jsonify(dummy_cases)

# POST 메서드: 새로운 케이스를 생성하여 더미 데이터에 추가

# 케이스 페이지
@app.route("/case")
def case():
    return render_template("case.html")

@app.route("/login")
def login():
    return render_template("login.html")

# 케이스 분석 페이지
@app.route("/case-analysis")
def case_analysis():
    return render_template("case_analysis.html")

if __name__ == '__main__':
    app.run(debug=True)
