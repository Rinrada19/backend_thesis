from flask import Blueprint, app, jsonify, request
from werkzeug.security import check_password_hash
import jwt
import datetime
from flask_login import login_required, current_user, login_user
from app import db
from services.auth_service import token_required
from models.user import User
from services import create_user, check_user_login
from werkzeug.security import generate_password_hash, check_password_hash
from services import generate_jwt

# สร้างฟังก์ชันสำหรับสร้าง blueprint
def create_users_bp():
    users_bp = Blueprint('users', __name__, url_prefix='/users')  # Add url_prefix here

    # สร้าง endpoint สำหรับดึงข้อมูลผู้ใช้
    @users_bp.route('', methods=['GET'])  # '/' becomes '/users'
    @token_required
    def get_users(user_id):  # รับ user_id ที่ถูกส่งจาก token_required
        try:
            # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
            users = User.query.filter_by(user_id=user_id).all()  # แสดงผลเฉพาะข้อมูลของ user ที่เกี่ยวข้อง
            if not users:
                return jsonify({"message": "No users found"}), 404  # ถ้าไม่มีผู้ใช้

            result = []
            for user in users:
                result.append({
                    'user_id': user.user_id,
                    'username': user.username,
                    'password': user.password,
                    'email': user.email,
                    'gender': user.gender,
                    'age': user.age,
                    'height': user.height,
                    'weight': user.weight,
                    'dietary_restriction': user.dietary_restriction,
                    'congenital_disease': user.congenital_disease,
                    'physical_activity': user.physical_activity,
                    'goal': user.goal,
                    'require_weight': user.require_weight,
                    'bmi': user.bmi,
                    'goal_cal': user.goal_cal,
                    'created_at': user.created_at,  # เพิ่มวันที่สร้าง
                    'updated_at': user.updated_at   # เพิ่มวันที่แก้ไขล่าสุด
                })
            return jsonify(result), 200  # ส่งกลับข้อมูลผู้ใช้พร้อม status 200
        
        except Exception as e:
            return jsonify({"message": "Error retrieving users", "error": str(e)}), 500


    # สร้าง endpoint สำหรับ login
    @users_bp.route('/login', methods=['POST'],endpoint='login')
    def login():
        data = request.get_json()  # รับข้อมูลจากคำขอ

        # รับ username และ password จากคำขอ
        username = data.get('username')
        password = data.get('password')

        # ตรวจสอบว่ามีการส่งข้อมูลหรือไม่
        if not all([username, password]):
            return jsonify({"message": "Username and password are required"}), 400

        # ตรวจสอบผู้ใช้
        user = check_user_login(username, password)
        
        if user:
            # สร้าง JWT สำหรับผู้ใช้
            token = generate_jwt(user)

            # คืนค่าข้อความสำเร็จและส่ง JWT กลับ
            return jsonify({
            "message": "Login successful",
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "gender": user.gender,
            "age": user.age,
            "height": user.height,
            "weight": user.weight,
            "dietary_restriction": user.dietary_restriction,
            "congenital_disease": user.congenital_disease,
            "physical_activity": user.physical_activity,
            "goal": user.goal,
            "require_weight": user.require_weight,
            "bmi": user.bmi,
            "goal_cal": user.goal_cal,
            "token": token  # ส่ง token กลับไป
        }), 200
        else:
            # ถ้าผู้ใช้หรือรหัสผ่านผิด คืนค่าข้อความผิดพลาด
            return jsonify({"message": "Invalid username or password"}), 401
        
    @users_bp.route('/protected', methods=['GET'])
    def protected():
        token = request.headers.get('Authorization')  # รับ token จาก headers
        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            # ลบคำว่า "Bearer " ออก
            token = token.split(" ")[1]
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = decoded['user_id']
            
            # ดำเนินการกับ user_id ที่ได้จาก JWT
            return jsonify({"message": f"Access granted for user {user_id}"}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401
    
    # สร้าง endpoint สำหรับดึงข้อมูล profile ของผู้ใช้ที่เข้าสู่ระบบแล้ว
    # @users_bp.route('/profile', methods=['GET'])
    # def profile():
    #     token = request.headers.get('Authorization')
    #     if not token:
    #         return jsonify({"message": "Token is missing!"}), 403
        
    #     try:
    #         # แยก Bearer token ออกจาก header
    #         token = token.split(" ")[1]
    #         decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    #         user_id = decoded['user_id']
            
    #         # ดึงข้อมูลผู้ใช้จากฐานข้อมูล
    #         user = User.query.get(user_id)
    #         if not user:
    #             return jsonify({"message": "User not found"}), 404
            
    #         return jsonify({
    #             "username": user.username,
    #             "email": user.email,
    #             "gender": user.gender,
    #             "age": user.age,
    #             "height": user.height,
    #             "weight": user.weight
    #         }), 200
    #     except jwt.ExpiredSignatureError:
    #         return jsonify({"message": "Token has expired"}), 401
    #     except jwt.InvalidTokenError:
    #         return jsonify({"message": "Invalid token"}), 401


    @users_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()

        # รับข้อมูลจากคำขอ
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        dietary_restriction = data.get('dietary_restriction', '')  # ใช้ค่า default
        congenital_disease = data.get('congenital_disease', '')  # ใช้ค่า default
        physical_activity = data.get('physical_activity')
        goal = data.get('goal')
        require_weight = data.get('require_weight')
        
        # คำนวณค่า BMI โดยใช้สูตร BMI = weight / (height / 100)^2
      

        # ตรวจสอบข้อมูลที่จำเป็น
        if not all([username, email, password, gender, age, height, weight, physical_activity, goal, require_weight]):
            return jsonify({"message": "All fields are required"}), 400

        # ตรวจสอบว่าอีเมลซ้ำ
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "Email already exists"}), 400

        # แฮชรหัสผ่าน
        hashed_password = generate_password_hash(password)

        # สร้างผู้ใช้ใหม่
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            dietary_restriction=dietary_restriction,
            congenital_disease=congenital_disease,
            physical_activity=physical_activity,
            goal=goal,
            require_weight=require_weight,
           
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user_id": new_user.user_id
        }), 201

    @users_bp.route('/check-username', methods=['POST'])
    def check_username():
        try:
            data = request.get_json()
            username = data.get('username')

            if not username:
                return jsonify({"message": "กรุณาส่ง username"}), 400

            user = User.query.filter_by(username=username).first()
            if user:
                return jsonify({"available": False, "message": "ชื่อผู้ใช้นี้ถูกใช้ไปแล้ว"}), 409

            return jsonify({"available": True, "message": "สามารถใช้ได้"}), 200

        except Exception as e:
            return jsonify({"message": "เกิดข้อผิดพลาด", "error": str(e)}), 500

    @users_bp.route('/check-email', methods=['POST'])
    def check_email():
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return jsonify({"message": "กรุณาส่ง email"}), 400

            user = User.query.filter_by(email=email).first()
            if user:
                return jsonify({"available": False, "message": "อีเมลนี้ถูกใช้ไปแล้ว"}), 409

            return jsonify({"available": True, "message": "สามารถใช้ได้"}), 200

        except Exception as e:
            return jsonify({"message": "เกิดข้อผิดพลาด", "error": str(e)}), 500




    return users_bp
