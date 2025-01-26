from flask import Blueprint, request, jsonify
from models.caloric_intake import CaloricIntake
from services.auth_service import token_required

# สร้าง Blueprint สำหรับ CaloricIntake API
caloric_intake_bp = Blueprint('caloric_intake', __name__)

# Endpoint สำหรับการดึงข้อมูล CaloricIntake ของผู้ใช้พร้อมกับการแบ่งหน้า
@caloric_intake_bp.route('/caloric_intake', methods=['GET'])
@token_required
def get_caloric_intake(user_id):
    try:
        # รับพารามิเตอร์ page และ per_page จาก query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # ดึงข้อมูลทั้งหมดจากฐานข้อมูลตาม user_id โดยใช้ pagination
        caloric_intake_paginated = CaloricIntake.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)

        # ดึงข้อมูลในหน้า (current page)
        result = []
        for caloric_intake in caloric_intake_paginated.items:
            result.append({
                'caloric_intake_id': caloric_intake.caloric_intake_id,
                'user_id': caloric_intake.user_id,
                'date': caloric_intake.date,
                'cal_goal': caloric_intake.cal_goal,
                'total_cal': caloric_intake.total_cal,
                'fat': caloric_intake.fat,
                'carb': caloric_intake.carb,
                'protein': caloric_intake.protein,
                'water': caloric_intake.water,
                'sugar': caloric_intake.sugar,
                'meal_eaten_id': caloric_intake.meal_eaten_id,
                'fat_goal': caloric_intake.fat_goal,
                'carb_goal': caloric_intake.carb_goal,
                'protein_goal': caloric_intake.protein_goal,
                'sugar_goal': caloric_intake.sugar_goal,
                'sodium_goal': caloric_intake.sodium_goal,
                'sodium': caloric_intake.sodium
            })

        return jsonify({
            'caloric_intake': result,
            'total': caloric_intake_paginated.total,  # ใช้จำนวนทั้งหมดจาก pagination
            'page': page,
            'pages': caloric_intake_paginated.pages  # ใช้จำนวนหน้าจาก pagination
        })

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@caloric_intake_bp.route('/caloric_intake/<int:id>', methods=['GET'])
@token_required
def get_caloric_intake_by_id(user_id, id):
    try:
        # ค้นหาข้อมูล CaloricIntake ที่มี caloric_intake_id ตรงกับที่ระบุใน URL
        caloric_intake = CaloricIntake.query.filter_by(user_id=user_id, caloric_intake_id=id).first()

        if caloric_intake is None:
            return jsonify({"message": "Caloric intake record not found"}), 404

        # สร้างผลลัพธ์ที่ต้องการแสดง
        result = {
            'caloric_intake_id': caloric_intake.caloric_intake_id,
            'user_id': caloric_intake.user_id,
            'date': caloric_intake.date,
            'cal_goal': caloric_intake.cal_goal,
            'total_cal': caloric_intake.total_cal,
            'fat': caloric_intake.fat,
            'carb': caloric_intake.carb,
            'protein': caloric_intake.protein,
            'water': caloric_intake.water,
            'sugar': caloric_intake.sugar,
            'meal_eaten_id': caloric_intake.meal_eaten_id,
            'fat_goal': caloric_intake.fat_goal,
            'carb_goal': caloric_intake.carb_goal,
            'protein_goal': caloric_intake.protein_goal,
            'sugar_goal': caloric_intake.sugar_goal,
            'sodium_goal': caloric_intake.sodium_goal,
            'sodium': caloric_intake.sodium
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
