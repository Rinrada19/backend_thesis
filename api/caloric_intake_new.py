from flask import Blueprint, request, jsonify
from sqlalchemy import func
from datetime import datetime, timedelta
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
        fat_goal = (cal_goal * 0.3) / 9;   # แปลงจาก kcal เป็นกรัม
        carb_goal = (cal_goal * 0.6) / 4;  # แปลงจาก kcal เป็นกรัม
        protein_goal = (cal_goal * 0.1) / 4;  # แปลงจาก kcal เป็นกรัม

        
        
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





@eat_today_bp.route('/eat_week', methods=['GET'])
@token_required
def get_eat_week(user_id):
    try:
        today = datetime.today()

        # หาวันแรกของสัปดาห์ (วันจันทร์)
        start_of_week = today - timedelta(days=(today.weekday() + 1) % 7)  # วันอาทิตย์
        end_of_week = start_of_week + timedelta(days=6)  # วันเสาร์


        # แปลงเป็น string format YYYY-MM-DD
        start_date_str = start_of_week.strftime('%Y-%m-%d')
        end_date_str = end_of_week.strftime('%Y-%m-%d')

        # ดึงเป้าหมายแคลอรี่ของผู้ใช้
        user = User.query.filter_by(user_id=user_id).first()
        cal_goal = user.goal_cal if user else 0

        # ดึงข้อมูล Meal ภายในช่วงสัปดาห์
        meals = Meal.query.filter(
            Meal.user_id == user_id,
            func.date(Meal.created_at) >= start_of_week,
            func.date(Meal.created_at) <= end_of_week
        ).all()

  
    

        # สร้าง dictionary จัดข้อมูลตามวันที่
        daily_calories = {}

        meals = Meal.query.filter(
                    Meal.user_id == user_id,
                    func.date(Meal.created_at) >= start_date_str,
                    func.date(Meal.created_at) <= end_date_str
                ).all()
        daily_calories = {}

        for meal in meals:
            date_str = meal.created_at.strftime('%Y-%m-%d')  # แปลงเป็น string (YYYY-MM-DD)
            daily_calories[date_str] = daily_calories.get(date_str, 0) + meal.cal  # รวมค่าแคลอรี่

        total_cal = sum(daily_calories.values())

        avg_cal_per_day = total_cal / 7  # แก้ให้เฉลี่ยจากวันที่มีข้อมูล

        # แสดงผลลัพธ์
        print("Calories by Date:", daily_calories)
        
        # แสดงผลลัพธ์ที่รวมแคลอรี่ของแต่ละวัน
       
        print("Mealtime Data:", meals)
        print(f"User ID: {user_id}, Start Date: {start_date_str}, End Date: {end_date_str}")


        # แปลงเป็น list
        details = [{"date": date, "calories": cal} for date, cal in daily_calories.items()]

        result = {
            "user_id": user_id,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "cal_goal": cal_goal,  
            "total_cal": total_cal,
            "avg_cal_per_day": avg_cal_per_day,
            "details": details
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
