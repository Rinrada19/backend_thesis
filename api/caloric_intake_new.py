from flask import Blueprint, request, jsonify
from sqlalchemy import func
from datetime import datetime
from services.auth_service import token_required
from app import db
from models.meal import Meal
from models.user import User
# สร้าง blueprint สำหรับ API
eat_today_bp = Blueprint('eat_today', __name__)

@eat_today_bp.route('/eat_today', methods=['POST'])
@token_required
def get_eat_today(user_id):  # รับ user_id จาก JWT
    try:
        # รับค่าจาก request body
        data = request.get_json()
        date_str = data.get('date')

        # ตรวจสอบวันที่ที่ได้รับ
        if not date_str:
            return jsonify({"message": "Date is required"}), 400

        # แปลงวันที่เป็น date object
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format, use YYYY-MM-DD"}), 400

        # ดึงข้อมูล user.
        user = User.query.filter_by(user_id=user_id).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        # ดึงข้อมูล meals ของ user ในวันที่กำหนด
        meals = Meal.query.filter(
            Meal.user_id == user_id,
            func.date(Meal.created_at) == date
        ).all()

        # คำนวณค่า total_cal และสารอาหารจากมื้ออาหาร
        total_cal = sum(meal.cal for meal in meals)
        fat = sum(meal.fat for meal in meals)
        carb = sum(meal.carb for meal in meals)
        protein = sum(meal.protein for meal in meals)
        sugar = sum(meal.sugar for meal in meals)
        sodium = sum(meal.sodium for meal in meals)

        # คำนวณเป้าหมาย
        cal_goal = user.goal_cal
        fat_goal = cal_goal * 0.3
        carb_goal = cal_goal * 0.6
        protein_goal = cal_goal * 0.1
        
        
        if 9 <= user.age <= 12:
            sodium_goal = 1175
        elif 13 <= user.age <= 18:
            sodium_goal = 1600
        elif 19 <= user.age <= 70:
            sodium_goal = 1475
        else:  # 71+
            sodium_goal = 1200

        # คำนวณ sugar_goal ตามอายุและระดับกิจกรรม
        if user.physical_activity in ['High', 'Very High']:
            sugar_goal = 32
        elif 6 <= user.age <= 13:
            sugar_goal = 16
        elif 14 <= user.age <= 25:
            sugar_goal = 24
        elif 25 <= user.age <= 60:
            sugar_goal = 16
        else:  # อายุมากกว่า 60
            sugar_goal = 16
            

        # สร้างผลลัพธ์
        result = {
            "user_id": user_id,
            "date": date_str,
            "cal_goal": cal_goal,
            "total_cal": total_cal,
            "fat": fat,
            "carb": carb,
            "protein": protein,
            "sugar": sugar,
            "sodium": sodium,
            "fat_goal": fat_goal,
            "carb_goal": carb_goal,
            "protein_goal": protein_goal,
            "sugar_goal": sugar_goal,
            "sodium_goal": sodium_goal
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
