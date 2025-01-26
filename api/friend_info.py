from flask import Blueprint, jsonify, request
from db import db
from models.friend_info import FriendInfo
from models.user import User
from services.auth_service import token_required
from sqlalchemy import func, text
from datetime import datetime
from models.meal import Meal

friendinfo_bp = Blueprint('friend_info', __name__)

@friendinfo_bp.route('/friend_info', methods=['GET'])
@token_required
def get_friend_info(user_id):
    # ใช้ SQLAlchemy เพื่อ query ข้อมูล
    sql = text("""
        SELECT 
            CASE 
                WHEN me.user_id = f.user_id THEN f.friend_id
                ELSE f.user_id
            END AS friend_id,
            CASE 
                WHEN me.user_id = f.user_id THEN f.user_id
                ELSE f.friend_id
            END AS user_id,
            me.meal_eaten_id,
            m.food_name,
            m.food_description,
            m.cal AS calories,
            u.goal_cal,
            SUM(m.cal) OVER (PARTITION BY me.user_id) AS total_calories,
            CASE 
                WHEN me.user_id = f.user_id THEN 'self'
                ELSE 'friend'
            END AS user_type
        FROM 
            public.meal_eaten me
        JOIN 
            public.meal m ON me.meal_id = m.meal_id
        JOIN 
            public.users u ON me.user_id = u.user_id
        JOIN 
            public.friend_info f ON (me.user_id = f.user_id OR me.user_id = f.friend_id)
        WHERE 
            me.user_id = :user_id 
        ORDER BY 
            me.user_id, me.created_at;
    """)

    # ดึงข้อมูลจากฐานข้อมูล
    result = db.session.execute(sql, {'user_id': user_id}).fetchall()

    if result:
        # กรองข้อมูลที่มี user_type เป็น 'friend' เท่านั้น
        formatted_result = [
            {
                'user_id': row.user_id, 
                'friend_id': row.friend_id,
                'meal_eaten_id': row.meal_eaten_id,
                'food_name': row.food_name,
                'food_description': row.food_description,
                'calories': row.calories,
                'total_calories': row.total_calories,
                'user_type': row.user_type,
            }
            for row in result if row.user_type == 'friend'  # กรองข้อมูลที่เป็น 'friend' เท่านั้น
        ]
        return jsonify(formatted_result)
    else:
        return jsonify({'error': 'No friend info found for this user'}), 404

@friendinfo_bp.route('/friend_info/<int:friend_id>', methods=['GET'])
@token_required
def get_today_meals_of_friend(user_id, friend_id):
    try:
        # ดึงวันที่ปัจจุบันใน timezone ของระบบ
        today = datetime.now().date()

        # ค้นหาข้อมูลมื้ออาหารที่ถูกสร้างในวันที่ปัจจุบันโดยเพื่อน
        meals_today = db.session.query(Meal).join(FriendInfo, (FriendInfo.friend_id == friend_id) | (FriendInfo.user_id == friend_id)).filter(
            func.date(Meal.created_at) == today  # กรองข้อมูลมื้ออาหารที่ถูกสร้างในวันนี้
        ).all()

        if not meals_today:
            return jsonify({"message": "No meals found for today for the friend!"}), 404

        # จัดเตรียมผลลัพธ์
        result = []
        for meal in meals_today:
            result.append({
                'meal_id': meal.meal_id,
                'food_name': meal.food_name,
                'cal': meal.cal,
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
