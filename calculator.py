from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    # Khởi tạo các giá trị ban đầu cho Form và Thông báo lỗi
    a_val = ''
    b_val = ''
    op_val = '+'
    
    err_a = ''
    err_b = ''
    result = ''
    
    if request.method == 'POST':
        # 1. Lấy dữ liệu gửi từ Form qua request.form
        a_val = request.form.get('a', '').strip()
        b_val = request.form.get('b', '').strip()
        op_val = request.form.get('op', '+')
        
        # Chuyển đổi dấu phẩy (2,5) thành dấu chấm (2.5) để xử lý số thực
        a_str = a_val.replace(',', '.')
        b_str = b_val.replace(',', '.')
        
        # 2. Validate đầu vào (Kiểm tra trống và kiểm tra định dạng số)
        has_error = False
        num_a = None
        num_b = None
        
        # Kiểm tra ô 'a'
        if not a_val:
            err_a = 'Không được để trống'
            has_error = True
        else:
            try:
                num_a = float(a_str)
            except ValueError:
                err_a = 'Vui lòng nhập một số.'
                has_error = True
                
        # Kiểm tra ô 'b'
        if not b_val:
            err_b = 'Không được để trống'
            has_error = True
        else:
            try:
                num_b = float(b_str)
            except ValueError:
                err_b = 'Vui lòng nhập một số.'
                has_error = True

        # Trường hợp cả 2 ô đều trống (Khớp theo bảng testcase: "Lỗi cả hai ô")
        if not a_val and not b_val:
            err_a = 'Lỗi cả hai ô'
            err_b = 'Lỗi cả hai ô'

        # 3. Thực hiện tính toán nếu không có lỗi validate ban đầu
        if not has_error:
            valid_operators = ['+', '-', '*', '/']
            
            # Kiểm tra toán tử hợp lệ (Tránh trường hợp bị sửa HTML/DevTools)
            if op_val not in valid_operators:
                result = 'Phép toán không hợp lệ.'
            elif op_val == '/' and num_b == 0:
                err_b = 'Không thể chia cho 0.'
            else:
                # Tính toán
                if op_val == '+':
                    res_num = num_a + num_b
                elif op_val == '-':
                    res_num = num_a - num_b
                elif op_val == '*':
                    res_num = num_a * num_b
                elif op_val == '/':
                    res_num = num_a / num_b
                
                # Định dạng số hiển thị (bỏ đuôi .0 nếu là số nguyên)
                def fmt(val):
                    return int(val) if val.is_integer() else val

                result = f"{fmt(num_a)} {op_val} {fmt(num_b)} = {fmt(res_num)}"

    # Truyền dữ liệu ngược lại giao diện để giữ nguyên dữ liệu sau khi submit
    return render_template(
        'calculator.html',
        a=a_val,
        b=b_val,
        op=op_val,
        err_a=err_a,
        err_b=err_b,
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)