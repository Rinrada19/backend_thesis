from flask import Blueprint, jsonify, request
from api.caloric_intake_new import get_eat_today
from db import db
from models.friend import Friend
from models.friend_info import FriendInfo
from models.user import User
from models.meal import Meal
from services.auth_service import token_required
from sqlalchemy import func, text
from datetime import datetime
from models.meal import Meal
from sqlalchemy import or_


friendinfo_bp = Blueprint('friend_info', __name__)



from sqlalchemy import or_

 # นำเข้าโมเดล Meal

# ฟังก์ชันสำหรับดึงข้อมูล meals ของเพื่อน
def get_meals(friend_id):
    # ดึงข้อมูล meals จากฐานข้อมูลที่เชื่อมโยงกับ friend_id
    meals = Meal.query.filter(Meal.user_id == friend_id).all()

    # หากไม่พบข้อมูล meals สำหรับ friend_id นี้
    if not meals:
        return []

    # คืนค่าข้อมูล meals ที่พบ
    return meals
@friendinfo_bp.route('/friend_info', methods=['GET'])
@token_required
def get_friend_info(user_id):
    try:
        # ดึงข้อมูลเพื่อนที่เกี่ยวข้องกับ user_id
        friends = db.session.query(Friend).filter(
            or_(Friend.user_id == user_id, Friend.friend_id == user_id)
        ).all()

        if not friends:
            return jsonify({"message": f"No friends found for user with ID: {user_id}"}), 404

        friend_ids = set()
        for friend in friends:
            # หารายชื่อเพื่อนจากทั้ง user_id และ friend_id
            if friend.user_id == user_id:
                friend_ids.add(friend.friend_id)
            else:
                friend_ids.add(friend.user_id)

        friend_data = []
        for friend_id in friend_ids:
            # ดึงข้อมูลของเพื่อนจากตาราง User
            friend_instance = User.query.get(friend_id)

            if friend_instance:
                # ดึงข้อมูล meals สำหรับเพื่อนจากฐานข้อมูล
                meals = db.session.query(Meal).filter(Meal.user_id == friend_id).all()

                # คำนวณ total_cal โดยการรวมค่า cal จาก meals
                total_cal = sum(meal.cal for meal in meals)

                # สร้างข้อมูลที่จะแสดงผล
                friend_meal_data = {
                    "friend_id": friend_id,
                    "friend_username": friend_instance.username,  # ใช้ข้อมูลจาก friend_instance
                    "goal_cal": friend_instance.goal_cal,  # ให้ใช้ cal_goal ตามที่เรากำหนดในโมเดล
                    "total_cal": total_cal
                }
                friend_data.append(friend_meal_data)
            else:
                friend_data.append({
                    "friend_id": friend_id,
                    "message": "เพื่อนไม่พบในระบบ"
                })

        return jsonify(friend_data), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


# @friendinfo_bp.route('/friend_info', methods=['GET'])
# @token_required
# def get_friend_info(user_id):
#     # ใช้ SQLAlchemy เพื่อ query ข้อมูล
#     sql = text("""
#         SELECT 
#             CASE 
#                 WHEN me.user_id = f.user_id THEN f.friend_id
#                 ELSE f.user_id
#             END AS friend_id,
#             CASE 
#                 WHEN me.user_id = f.user_id THEN f.user_id
#                 ELSE f.friend_id
#             END AS user_id,
#             me.meal_eaten_id,
#             m.food_name,
#             m.food_description,
#             m.cal AS calories,
#             u.goal_cal,
#             SUM(m.cal) OVER (PARTITION BY me.user_id) AS total_calories,
#             CASE 
#                 WHEN me.user_id = f.user_id THEN 'self'
#                 ELSE 'friend'
#             END AS user_type
#         FROM 
#             public.meal_eaten me
#         JOIN 
#             public.meal m ON me.meal_id = m.meal_id
#         JOIN 
#             public.users u ON me.user_id = u.user_id
#         JOIN 
#             public.friend_info f ON (me.user_id = f.user_id OR me.user_id = f.friend_id)
#         WHERE 
#             me.user_id = :user_id 
#         ORDER BY 
#             me.user_id, me.created_at;
#     """)

#     # ดึงข้อมูลจากฐานข้อมูล
#     result = db.session.execute(sql, {'user_id': user_id}).fetchall()

#     if result:
#         # กรองข้อมูลที่มี user_type เป็น 'friend' เท่านั้น
#         formatted_result = [
#             {
#                 'user_id': row.user_id, 
#                 'friend_id': row.friend_id,
#                 'meal_eaten_id': row.meal_eaten_id,
#                 'food_name': row.food_name,
#                 'food_description': row.food_description,
#                 'calories': row.calories,
#                 'total_calories': row.total_calories,
#                 'user_type': row.user_type,
#             }
#             for row in result if row.user_type == 'friend'  # กรองข้อมูลที่เป็น 'friend' เท่านั้น
#         ]
#         return jsonify(formatted_result)
#     else:
#         return jsonify({'error': 'No friend info found for this user'}), 404


from datetime import datetime
from sqlalchemy import func

@friendinfo_bp.route('/friend_info/<int:friend_id>', methods=['GET'])
@token_required
def get_today_meals_of_friend(user_id, friend_id):
    try:
        # ดึงวันที่ปัจจุบันใน timezone ของระบบ
        today = datetime.now().date()

        # ค้นหาข้อมูลมื้ออาหารที่ถูกสร้างในวันที่ปัจจุบันของเพื่อน
        meals_today = db.session.query(Meal).filter(
            Meal.user_id == friend_id,  # เลือกเพื่อนที่ต้องการ
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
