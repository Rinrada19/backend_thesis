from flask import Blueprint, jsonify, request
from db import db
from models.saved_meal import SavedMeal
from services.auth_service import token_required
from datetime import datetime
from models.meal import Meal

saved_meal_bp = Blueprint('saved_meal', __name__)

# GET all saved meals
@saved_meal_bp.route('/saved_meals', methods=['GET'])
@token_required
def get_saved_meals(user_id):
    try:
        # ดึงข้อมูลทุกรายการจาก SavedMeal และเชื่อมโยงกับข้อมูลในตาราง meal
        saved_meals = db.session.query(SavedMeal, Meal).join(Meal, SavedMeal.meal_id == Meal.meal_id).filter(SavedMeal.user_id == user_id).all()

        if not saved_meals:
            return jsonify({'message': 'No saved meals found for this user'}), 404

        # ส่งผลลัพธ์เป็นรายการของอ็อบเจ็กต์ที่มีข้อมูลจาก SavedMeal และ meal_name จาก Meal
        result = [
            {
                "saved_meal_id": meal[0].saved_meal_id,
                "user_id": meal[0].user_id,
                "meal_id": meal[0].meal_id,
                "food_name": meal[1].food_name,  # ชื่อของ meal จากตาราง Meal
                "create_at": meal[0].create_at
            } for meal in saved_meals
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


# POST new saved meal

@saved_meal_bp.route('/saved_meal', methods=['POST'])
@token_required
def save_meal(user_id):
    try:
        # รับค่าจาก body ของ request
        data = request.get_json()

        # ดึงข้อมูลจาก body ของ request
        meal_id = data.get('meal_id')
        create_at = data.get('create_at', datetime.now())  # กำหนด default เป็นเวลาปัจจุบันหากไม่ได้ส่ง
       
        # ตรวจสอบว่า meal_id และ create_at ถูกส่งมา
        if not meal_id:
            return jsonify({"error": "meal_id is required"}), 400

        # ตรวจสอบว่ามี saved meal ที่มี meal_id และ user_id เดียวกันอยู่แล้วหรือไม่
        existing_saved_meal = SavedMeal.query.filter_by(user_id=user_id, meal_id=meal_id).first()

        if existing_saved_meal:
            return jsonify({"error": "Saved meal already exists for this user"}), 400

        # สร้างอ็อบเจ็กต์ SavedMeal
        new_saved_meal = SavedMeal(
            user_id=user_id,  # ใช้ user_id ที่มาจาก token
            meal_id=meal_id,
            create_at=create_at
        )

        # เพิ่มข้อมูลลงในฐานข้อมูล
        db.session.add(new_saved_meal)
        db.session.commit()

        return jsonify({"message": "Saved meal successfully!"}), 201

    except Exception as e:
        db.session.rollback()  # หากเกิดข้อผิดพลาดจะ rollback ข้อมูล
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@saved_meal_bp.route('/saved_meal/<int:saved_meal_id>', methods=['DELETE'])
@token_required
def delete_saved_meal(user_id, saved_meal_id):
    try:
        # ค้นหาข้อมูล saved_meal ที่ต้องการลบ
        saved_meal = SavedMeal.query.filter_by(saved_meal_id=saved_meal_id, user_id=user_id).first()

        if not saved_meal:
            return jsonify({'message': 'Saved meal not found for this user'}), 404

        # ลบข้อมูล saved_meal
        db.session.delete(saved_meal)
        db.session.commit()

        return jsonify({'message': 'Saved meal deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()  # หากเกิดข้อผิดพลาดจะ rollback ข้อมูล
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


# GET saved meal by ID
@saved_meal_bp.route('/saved_meals/<int:saved_meal_id>', methods=['GET'])
@token_required
def get_saved_meal_by_id(user_id, saved_meal_id):
    try:
        # ค้นหาข้อมูล saved meal โดยใช้ saved_meal_id และเชื่อมโยงกับ Meal
        saved_meal = db.session.query(SavedMeal, Meal).join(Meal, SavedMeal.meal_id == Meal.meal_id).filter(SavedMeal.saved_meal_id == saved_meal_id, SavedMeal.user_id == user_id).first()

        if not saved_meal:
            return jsonify({'message': 'Saved meal not found for this user'}), 404

        # ดึงข้อมูลจากทั้ง SavedMeal และ Meal แล้วแสดงข้อมูลตามที่ต้องการ
        result = {
            "saved_meal_id": saved_meal[0].saved_meal_id,
            "user_id": saved_meal[0].user_id,
            "meal_id": saved_meal[0].meal_id,
            "meal_details": {
                'food_name': saved_meal[1].food_name,
                'food_description': saved_meal[1].food_description,
                'fat': saved_meal[1].fat,
                'carb': saved_meal[1].carb,
                'protein': saved_meal[1].protein,
                'cal': saved_meal[1].cal,
                'sugar': saved_meal[1].sugar,
                'sodium': saved_meal[1].sodium,
                'type': saved_meal[1].type,
                'rice': saved_meal[1].rice,
                'egg': saved_meal[1].egg,
                'meal_type': saved_meal[1].meal_type
            },
            "create_at": saved_meal[0].create_at
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
