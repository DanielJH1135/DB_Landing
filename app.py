from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import requests  # 구글 웹앱과 통신하기 위해 필요합니다.

app = Flask(__name__)
app.secret_key = 'vercel_secret_key_pro'

# ⚠️ [매우 중요] 2번 단계에서 생성할 구글 배포 URL을 여기에 붙여넣으세요!
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxJxSowfOJ6EGKLoAihng8RqtDstseZTwZNCaC0E-0qTC9sIQxdscI9ig_fj8v5SnH3xg/exec"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        message = request.form.get('message', '')
        agree = request.form.get('agree')
        
        if not agree:
            flash('개인정보 수집 동의가 필요합니다.', 'error')
            return redirect(url_for('index'))
            
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 구글 스프레드시트로 보낼 데이터 가공
        payload = {
            'time': current_time,
            'name': name,
            'phone': phone,
            'message': message
        }
        
        try:
            # Vercel 서버에서 구글 스크립트로 데이터 전송 (안전하게 외부 저장)
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
