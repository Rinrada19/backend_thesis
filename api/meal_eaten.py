from flask import Blueprint, request, jsonify
from models.meal_eaten import MealEaten
from services.auth_service import token_required

# สร้าง Blueprint สำหรับ MealEaten API
meal_eaten_bp = Blueprint('meal_eaten', __name__)

# Endpoint สำหรับการดึงข้อมูล MealEaten ของผู้ใช้พร้อมกับการแบ่งหน้า
@meal_eaten_bp.route('/meal_eaten', methods=['GET'])
@token_required
def get_meals_eaten(user_id):
    try:
        # รับพารามิเตอร์ page และ per_page จาก query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # ดึงข้อมูลทั้งหมดจากฐานข้อมูลตาม user_id
        meals_eaten = MealEaten.query.filter_by(user_id=user_id).all()

        # แบ่งข้อมูลด้วยการคำนวณเอง (pagination)
        start = (page - 1) * per_page
        end = start + per_page
        meals_eaten_paginated = meals_eaten[start:end]

        result = []
        for meal_eaten in meals_eaten_paginated:
            result.append({
                'meal_eaten_id': meal_eaten.meal_eaten_id,
                'created_at': meal_eaten.created_at,
                'meal_id': meal_eaten.meal_id,
                'user_id': meal_eaten.user_id
            })

        return jsonify({
            'meal_eaten': result,
            'total': len(meals_eaten),
            'page': page,
            'pages': (len(meals_eaten) // per_page) + 1  # คำนวณจำนวนหน้า
        })

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
