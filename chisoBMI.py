from flask import Flask, render_template, request

app = Flask(__name__)

def validate_input(val_str, name, min_val, max_val):
    val_str = val_str.strip()
    if not val_str:
        return None, f"Lỗi ô {name}: Không được để trống"
    
    # Chấp nhận dấu phẩy thập phân
    val_clean = val_str.replace(',', '.')
    
    try:
        val = float(val_clean)
    except ValueError:
        return None, f"Lỗi ô {name}: Vui lòng nhập một số."
    
    # Kiểm tra trường hợp nhập mét thay vì cm (vd: 1.70)
    if name == 'chiều cao' and val < 3.0:
        return None, f"Giá trị phải từ {min_val} đến {max_val}. (nhập mét thay vì cm)"
        
    if val < min_val or val > max_val:
        return None, f"Lỗi ô {name}: Giá trị phải từ {min_val} đến {max_val}."
    
    return val, ""

@app.route('/', methods=['GET', 'POST'])
def calculate_bmi():
    cao_val = ''
    nang_val = ''
    
    err_cao = ''
    err_nang = ''
    
    result = None
    
    if request.method == 'POST':
        # 1. Lấy dữ liệu từ request.form
        cao_val = request.form.get('cao', '')
        nang_val = request.form.get('nang', '')
        
        # 2. Validate đầu vào (Chiều cao: 50-250, Cân nặng: 10-300)
        h_cm, err_cao_msg = validate_input(cao_val, 'chiều cao', 50, 250)
        w_kg, err_nang_msg = validate_input(nang_val, 'cân nặng', 10, 300)
        
        # Kiểm tra nếu cả hai ô đều trống
        if not cao_val.strip() and not nang_val.strip():
            err_cao = 'Lỗi cả hai ô'
            err_nang = 'Lỗi cả hai ô'
        else:
            err_cao = err_cao_msg
            err_nang = err_nang_msg
            
        # 3. Tính toán nếu dữ liệu hợp lệ
        if h_cm is not None and w_kg is not None:
            h_m = h_cm / 100.0  # Đổi cm sang m
            bmi = round(w_kg / (h_m ** 2), 1)  # Làm tròn 1 chữ số thập phân
            
            # Phân loại theo chuẩn châu Á
            if bmi < 18.5:
                category = "Thiếu cân"
                color_class = "warning"  # Màu vàng (Bootstrap text-warning / alert-warning)
            elif bmi < 23:
                category = "Bình thường"
                color_class = "success"  # Màu xanh
            elif bmi < 25:
                category = "Thừa cân"
                color_class = "warning"  # Màu vàng
            else:
                category = "Béo phí"
                color_class = "danger"   # Màu đỏ
                
            # Cân nặng nên có tương ứng với BMI từ 18.5 đến 22.9
            min_weight = round(18.5 * (h_m ** 2), 1)
            max_weight = round(22.9 * (h_m ** 2), 1)
            
            result = {
                'bmi': bmi,
                'category': category,
                'color': color_class,
                'min_w': min_weight,
                'max_w': max_weight
            }

    return render_template(
        'chisoBMI.html',
        cao=cao_val,
        nang=nang_val,
        err_cao=err_cao,
        err_nang=err_nang,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)