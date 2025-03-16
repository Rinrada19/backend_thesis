import uuid
from flask import Blueprint, request, jsonify, current_app
import jwt
import datetime
from flask_mail import Message
from models.user import User
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from services.services import blacklist_token, is_token_valid

reset_pass_bp = Blueprint('reset_pass', __name__)

SECRET_KEY = "your_secret_key"  # เปลี่ยนเป็นค่า SECRET_KEY ของคุณ

# ฟังก์ชันสร้าง Token สำหรับ Reset Password
def create_reset_token(email, jti):
    jti = str(uuid.uuid4())
    payload = {
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # เพิ่ม , หลัง exp
        'iat': datetime.datetime.utcnow(),  # เพิ่มการใช้ datetime.datetime.utcnow() และเพิ่ม , หลัง
        'jti': jti  # เพิ่ม jti ลงใน payload
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def create_reset_url(token):
    if os.environ.get('FLASK_ENV') == 'development':
        return f'http://localhost:3000/reset-password/{token}'  # ใช้ token ใน URL
    else:
        return f'https://kakaloly.vercel.app/reset-password/{token}'  # ใช้ token ใน URL

# ฟังก์ชันตรวจสอบว่าอีเมลมีในฐานข้อมูลหรือไม่
def email_in_database(email):
    return User.query.filter_by(email=email).first() is not None

# ฟังก์ชันส่งอีเมลรีเซ็ตรหัสผ่าน
def send_reset_email(email, reset_url):
    mail = current_app.extensions['mail']
 
    msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"""
    สวัสดีค่ะ/ครับ,

    เราได้รับคำขอให้รีเซ็ตรหัสผ่านสำหรับบัญชีของคุณ

    กรุณาคลิกลิงก์ด้านล่างเพื่อรีเซ็ตรหัสผ่าน:

    {reset_url}

    ลิงก์นี้จะหมดอายุใน 1 ชั่วโมง เพื่อความปลอดภัยของคุณ

    ขอบคุณค่ะ/ครับ,
    KAKALOLY
    """
 
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# Endpoint ส่งอีเมล
@reset_pass_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email or not email_in_database(email):
        return jsonify({"message": "Email not found"}), 400
    
    jti = str(uuid.uuid4())  # สร้าง jti ที่ไม่ซ้ำกัน
    token = create_reset_token(email, jti)  # สร้าง token
    reset_url = create_reset_url(token)  # สร้าง URL ด้วย token

    if send_reset_email(email, reset_url):  # ส่ง reset_url
        return jsonify({"message": "Password reset link has been sent"}), 200
    else:
        return jsonify({"message": "Failed to send email"}), 500


# ฟังก์ชันรีเซ็ตรหัสผ่าน
# ฟังก์ชันรีเซ็ตรหัสผ่าน
@reset_pass_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    if not token or not new_password:
        return jsonify({"message": "Token and new password are required"}), 400

    try:
        # ตรวจสอบ token และ decode
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email = decoded_token.get('email')
        jti = decoded_token.get("jti")

        if not jti:
            return jsonify({"message": "Invalid token: No JTI found"}), 400

        # ค้นหาผู้ใช้
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # ตรวจสอบว่า Token ถูก Blacklist หรือไม่
        if is_token_valid(decoded_token, user) == False:
            return jsonify({"message": "Token has been blacklisted"}), 400

        # อัปเดตรหัสผ่าน
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        db.session.commit()

        # บล็อก Token เก่า
        blacklist_token(user, jti)

        return jsonify({"message": "Password has been successfully reset"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 400
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 400


# ฟังก์ชันอัพเดทรหัสผ่าน
def update_password_in_db(email, new_password):
    user = User.query.filter_by(email=email).first()
    if user:
        # เข้ารหัสรหัสผ่านใหม่
        hashed_password = generate_password_hash(new_password)
        user.password = hashed_password
        db.session.commit()

        # ตรวจสอบว่าอัพเดตแล้วจริงหรือไม่
        updated_user = User.query.filter_by(email=email).first()
        print(f"Password updated to: {updated_user.password}")  # ตรวจสอบว่ารหัสผ่านใหม่ถูกบันทึกหรือไม่