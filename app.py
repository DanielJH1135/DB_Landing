from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'vercel_secret_key_pro'

# ⚠️ [필수] 구글 배포 웹앱 URL을 기존 주소 그대로 여기에 다시 붙여넣으세요!
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxJxSowfOJ6EGKLoAihng8RqtDstseZTwZNCaC0E-0qTC9sIQxdscI9ig_fj8v5SnH3xg/exec"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        package = request.form.get('package')
        duration = request.form.get('duration')
        
        # 년/월/일 조합하여 하나의 날짜 문자열로 만들기
        year = request.form.get('start_year')
        month = request.form.get('start_month')
        day = request.form.get('start_day')
        start_date = f"{year}년 {month}월 {day}일"
        
        email = request.form.get('email')
        agree = request.form.get('agree')
        
        if not agree:
            flash('개인정보 수집 동의가 필요합니다.', 'error')
            return redirect(url_for('index'))
            
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 새롭게 설계된 데이터 구조 전송
        payload = {
            'time': current_time,
            'name': name,
            'phone': phone,
            'package': package,
            'duration': duration,
            'start_date': start_date,
            'email': email
        }
        
        try:
            response = requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=10)
            if response.status_code == 200:
                flash('상담 신청이 정상적으로 접수되었습니다. 곧 연락드리겠습니다!', 'success')
            else:
                flash('데이터 전송에 실패했습니다. 다시 시도해 주세요.', 'error')
        except Exception as e:
            flash(f'시스템 오류가 발생했습니다: {str(e)}', 'error')
            
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
