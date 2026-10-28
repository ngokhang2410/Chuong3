from flask import Flask, render_template, request

app = Flask(__name__)

# Viết một hàm kiểm tra dùng chung cho cả 3 ô (CC, GK, CK)
def validate_score(val_str, name):
    val_str = val_str.strip()
    if not val_str:
        return None, f"Lỗi ô {name}: Không được để trống"
    
    # Chấp nhận dấu phẩy thập phân
    val_clean = val_str.replace(',', '.')
    
    try:
        score = float(val_clean)
    except ValueError:
        return None, f"Lỗi ở {name}: Vui lòng nhập một số."
    
    # Kiểm tra miền giá trị từ 0 đến 10
    if score < 0 or score > 10:
        return None, f"Lỗi ở {name}: Điểm phải từ 0 đến 10."
    
    return score, ""

@app.route('/', methods=['GET', 'POST'])
def grade_calculator():
    cc_val = ''
    gk_val = ''
    ck_val = ''
    
    err_cc = ''
    err_gk = ''
    err_ck = ''
    
    result = ''
    
    if request.method == 'POST':
        # 1. Lấy dữ liệu từ Form
        cc_val = request.form.get('cc', '')
        gk_val = request.form.get('gk', '')
        ck_val = request.form.get('ck', '')
        
        # 2. Sử dụng hàm dùng chung để validate từng ô
        score_cc, err_cc_msg = validate_score(cc_val, 'CC')
        score_gk, err_gk_msg = validate_score(gk_val, 'GK')
        score_ck, err_ck_msg = validate_score(ck_val, 'CK')
        
        # Kiểm tra trường hợp cả 3 ô đều trống
        if not cc_val.strip() and not gk_val.strip() and not ck_val.strip():
            err_cc = 'Lỗi cả 3 ô'
            err_gk = 'Lỗi cả 3 ô'
            err_ck = 'Lỗi cả 3 ô'
        else:
            err_cc = err_cc_msg
            err_gk = err_gk_msg
            err_ck = err_ck_msg
        
        # 3. Nếu cả 3 ô đều hợp lệ -> Tính điểm học phần
        if score_cc is not None and score_gk is not None and score_ck is not None:
            # Tính điểm trung bình theo trọng số: CC (10%), GK (30%), CK (60%)
            tb = score_cc * 0.1 + score_gk * 0.3 + score_ck * 0.6
            tb_round = round(tb, 1) # Làm tròn 1 chữ số thập phân
            
            # Xếp loại điểm chữ (Kiểm tra điểm liệt cuối kỳ < 1)
            if score_ck < 1:
                letter = 'F (điểm thi dưới 1)'
            elif tb_round >= 8.5:
                letter = 'A'
            elif tb_round >= 7.0:
                letter = 'B'
            elif tb_round >= 5.5:
                letter = 'C'
            elif tb_round >= 4.0:
                letter = 'D'
            else:
                letter = 'F'
                
            result = f"{tb_round} - {letter}"

    return render_template(
        'diemhocphan.html',
        cc=cc_val,
        gk=gk_val,
        ck=ck_val,
        err_cc=err_cc,
        err_gk=err_gk,
        err_ck=err_ck,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)