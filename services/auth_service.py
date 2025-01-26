import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app


SECRET_KEY = current_app.config['SECRET_KEY']  # ใช้ค่า SECRET_KEY จาก config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("Token required decorator is being called")  # เพิ่ม print ที่จุดนี้
        token = None

        if 'Authorization' in request.headers:
            print("Authorization header found")  # ถ้ามี Authorization header
            try:
                token = request.headers['Authorization'].split(" ")[1]  # แยก Bearer <token>
                print(f"Token: {token}")  # พิมพ์ค่า token ที่ได้รับ
                decoded_payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                print(f"Decoded payload: {decoded_payload}")  # พิมพ์ decoded payload
                user_id = decoded_payload.get('user_id')

                if not user_id:
                    return jsonify({"message": "Invalid token: No user_id found"}), 401
                print(f"User ID: {user_id}")  # พิมพ์ user_id
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401
        else:
            print("Authorization header not found")  # ถ้าไม่มี Authorization header
            return jsonify({"message": "Token is missing"}), 401

        return f(user_id, *args, **kwargs)  # ส่ง user_id ไปยังฟังก์ชันหลัก
    return decorated


def create_token(user_id):
    """สร้าง JWT token สำหรับผู้ใช้"""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)  # หมดอายุใน 30 วัน
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    """ถอดรหัส JWT token เพื่อดึง user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # ถ้าโทเค็นหมดอายุ
    except jwt.InvalidTokenError:
        return None  # ถ้าโทเค็นไม่ถูกต้อง
