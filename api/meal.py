import jwt
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app import db
from models.meal import Meal
from sqlalchemy.exc import IntegrityError
from functools import wraps
from datetime import datetime, timedelta
from services.auth_service import token_required


# คีย์ลับที่ใช้ในการเข้ารหัสและถอดรหัส JWT
SECRET_KEY = "your_secret_key"  # ควรเปลี่ยนเป็นคีย์ที่ปลอดภัย

# ฟังก์ชันสำหรับตรวจสอบ JWT และดึงข้อมูล user_id


def create_meal_bp():
    meal_bp = Blueprint('meal', __name__)

    # Endpoint สำหรับการดึงข้อมูลทั้งหมดของ Meals พร้อมกับการแบ่งหน้า
    @meal_bp.route('/meals', methods=['GET'])
    @token_required
    def get_meals(user_id):
        print("This is the get_meals route")
        try:
            # ดึงข้อมูลทั้งหมดจากฐานข้อมูล
            meals = Meal.query.filter_by(user_id=user_id).order_by(Meal.created_at.desc()).all()  # ใช้ order_by() เพื่อเรียงลำดับ

            result = []
            for meal in meals:
                result.append({
                    'meal_id': meal.meal_id,
                    'food_name': meal.food_name,
                    'food_description': meal.food_description,
                    'fat': meal.fat,
                    'carb': meal.carb,
                    'protein': meal.protein,
                    'cal': meal.cal,
                    'sugar': meal.sugar,
                    'sodium': meal.sodium,
                    'type': meal.type,
                    'rice': meal.rice,
                    'egg': meal.egg,
                    'meal_type': meal.meal_type
                })

            # ส่งกลับข้อมูลทั้งหมด
            return jsonify({
                'meals': result,
                'total': len(meals)  # จำนวนทั้งหมดของข้อมูล
            })

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500



    @meal_bp.route('/meals/today', methods=['GET'])
    @token_required
    def get_today_meals(user_id):
        try:
            # ดึงวันที่ปัจจุบันใน timezone ของระบบ
            today = datetime.now().date()

            # ค้นหาข้อมูลมื้ออาหารของผู้ใช้ที่ถูกสร้างในวันที่ปัจจุบัน
            meals_today = Meal.query.filter(
                func.date(Meal.created_at) == today,
                Meal.user_id == user_id  # กรองข้อมูลตาม user_id
            ).all()

            if not meals_today:
                return jsonify({"meals": []}), 200

            # จัดเตรียมผลลัพธ์
            result = []
            for meal in meals_today:
                result.append({
                    'meal_id': meal.meal_id,
                    'food_name': meal.food_name,
                    'food_description': meal.food_description,
                    'fat': meal.fat,
                    'carb': meal.carb,
                    'protein': meal.protein,
                    'cal': meal.cal,
                    'sugar': meal.sugar,
                    'sodium': meal.sodium,
                    'type': meal.type,
                    'rice': meal.rice,
                    'egg': meal.egg,
                    'meal_type': meal.meal_type,
                    'created_at': meal.created_at.strftime('%Y-%m-%d %H:%M:%S')  # แปลงเป็น string เพื่อแสดงผล
                })

            return jsonify({
                'meals': result,
                'total': len(meals_today)
            }), 200

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    
    
    
    @meal_bp.route('/meals/by_date', methods=['GET'])  # ใช้ GET method
    @token_required
    def get_meals_by_date(user_id):
        try:
            # ดึงค่าของ date จาก query parameter
            date_str = request.args.get('date')

            if not date_str:
                return jsonify({"message": "Date is required!"}), 400

            # แปลงวันที่ที่ได้รับจาก string เป็น datetime.date
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

            # ค้นหาข้อมูลมื้ออาหารที่ถูกสร้างในวันที่ที่ระบุ และเป็นของ user_id ที่กำหนด
            meals_on_date = Meal.query.filter(
                func.date(Meal.created_at) == target_date,
                Meal.user_id == user_id  # กรองโดยใช้ user_id
            ).all()

            if not meals_on_date:
                return jsonify({"message": f"No meals found for {target_date}!"}), 404

            # จัดเตรียมผลลัพธ์
            result = []
            for meal in meals_on_date:
                result.append({
                    'meal_id': meal.meal_id,
                    'food_name': meal.food_name,
                    'food_description': meal.food_description,
                    'fat': meal.fat,
                    'carb': meal.carb,
                    'protein': meal.protein,
                    'cal': meal.cal,
                    'sugar': meal.sugar,
                    'sodium': meal.sodium,
                    'type': meal.type,
                    'rice': meal.rice,
                    'egg': meal.egg,
                    'meal_type': meal.meal_type,
                    'created_at': meal.created_at.strftime('%Y-%m-%d %H:%M:%S')  # แปลงเป็น string เพื่อแสดงผล
                })

            return jsonify({
                'meals': result,
                'total': len(meals_on_date)
            }), 200

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    
    @meal_bp.route('/meals/<int:id>', methods=['GET'])
    @token_required
    def get_meal_by_id(user_id, id):
        print("This is the get_meal_by_id route")
        try:
            # ค้นหามื้ออาหารที่มี meal_id ตรงกับที่กำหนดใน URL
            meal = Meal.query.get(id)

            if meal is None:
                return jsonify({"message": "Meal not found"}), 404

            result = {
                'meal_id': meal.meal_id,
                'food_name': meal.food_name,
                'food_description': meal.food_description,
                'fat': meal.fat,
                'carb': meal.carb,
                'protein': meal.protein,
                'cal': meal.cal,
                'sugar': meal.sugar,
                'sodium': meal.sodium,
                'type': meal.type,
                'rice': meal.rice,
                'egg': meal.egg,
                'meal_type': meal.meal_type
            }

            # ส่งกลับข้อมูลมื้ออาหาร
            return jsonify(result)

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    # Endpoint สำหรับการสร้าง Meal ใหม่
    @meal_bp.route('/meals', methods=['POST'])
    @token_required  # ใช้ decorator สำหรับตรวจสอบ token
    def create_meal(user_id):
        try:
            # รับข้อมูลจาก body ของ request
            data = request.get_json()

            # ตรวจสอบว่ามีข้อมูลที่จำเป็นครบถ้วนหรือไม่
            if not data.get('food_name') or not data.get('food_description') or not data.get('type'):
                return jsonify({"message": "Missing required fields!"}), 400
          

            # สร้าง Meal ใหม่ โดยใช้ user_id จาก JWT token
            new_meal = Meal(
                food_name=data['food_name'],
                food_description=data['food_description'],
                fat=data.get('fat', 0),
                carb=data.get('carb', 0),
                protein=data.get('protein', 0),
                cal=data.get('cal', 0),
                sugar=data.get('sugar', 0),
                sodium=data.get('sodium', 0),
                type=data['type'],  # เปลี่ยนจาก 'food_type' เป็น 'type'
                rice=data.get('rice'),
                egg=data.get('egg'),
                meal_type=data.get('meal_type'),
                user_id=user_id  # ใช้ user_id ที่ได้จาก JWT
            )



            # เพิ่มข้อมูลใหม่เข้าไปในฐานข้อมูล
            db.session.add(new_meal)
            db.session.commit()

            return jsonify({"message": "Meal created successfully!", "meal_id": new_meal.meal_id}), 201

        except IntegrityError as e:
            db.session.rollback()  # Rollback หากเกิดข้อผิดพลาดในการบันทึก
            return jsonify({"message": "Error creating meal", "error": str(e)}), 400

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500


    # Endpoint สำหรับการลบ Meal
    @meal_bp.route('/meals/<int:meal_id>', methods=['DELETE'])
    @token_required  # ใช้ decorator สำหรับตรวจสอบ token
    def delete_meal(user_id, meal_id):
        try:
            # ค้นหา meal ตาม meal_id ที่ระบุ
            meal_to_delete = Meal.query.get(meal_id)

            # หากไม่พบ meal ที่จะลบ
            if not meal_to_delete:
                return jsonify({"message": "Meal not found!"}), 404

            # ตรวจสอบว่า user_id ที่มาจาก JWT ตรงกับ user_id ของ meal ที่จะลบ
            if meal_to_delete.user_id != user_id:
                return jsonify({"message": "You are not authorized to delete this meal!"}), 403

            # ลบ meal ออกจากฐานข้อมูล
            db.session.delete(meal_to_delete)
            db.session.commit()

            return jsonify({"message": "Meal deleted successfully!"}), 200

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500


    return meal_bp
