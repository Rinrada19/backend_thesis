# utils.py or services.py

from flask import current_app  # นำเข้า current_app
from app import db

from models.user import User
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import jwt
import datetime


def generate_jwt(user):
    payload = {
        'user_id': user.user_id,  # เก็บ user_id ใน payload
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # กำหนดเวลา expired
    }
    
    # ใช้ current_app แทน app
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')  # เข้ารหัสด้วย SECRET_KEY
    return token

def create_user(username, password, email):
    # แฮชรหัสผ่านก่อนที่จะบันทึกลงฐานข้อมูล
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user



def check_user_login(username, password):
    user = User.query.filter_by(username=username).first()  # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
    if user:
        print(f"User found: {user.username}")
        print(f"Password entered: {password}")
        print(f"Password in DB: {user.password}")
        if check_password_hash(user.password, password):
            return user
    return None

def blacklist_token(user, jti):
    # ตรวจสอบว่า user.blacklisted_jti เป็นลิสต์หรือไม่
    if not isinstance(user.blacklisted_jti, list):
        user.blacklisted_jti = []  # ถ้าไม่เป็นลิสต์ให้กำหนดเป็นลิสต์ว่าง
    
    # เพิ่ม jti ใน blacklisted_jti
    user.blacklisted_jti.append(jti)

def is_token_valid(decoded_token, user):
    jti = decoded_token.get('jti')
    
    # ตรวจสอบว่า user.blacklisted_jti เป็น None หรือไม่
    if user.blacklisted_jti is None:
        user.blacklisted_jti = []  # ถ้าเป็น None ให้กำหนดให้เป็นลิสต์ว่าง
    
    # ตรวจสอบว่า jti อยู่ใน blacklisted_jti หรือไม่
    if jti in user.blacklisted_jti:
        return False
    return True

