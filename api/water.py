from flask import Blueprint, request, jsonify
from app import db
from models.water import WaterIntake
from datetime import datetime
from services.auth_service import token_required

# สร้าง Blueprint
water_intake_bp = Blueprint('water_intake', __name__)

# GET: ดึงข้อมูลน้ำที่ดื่มตามวันที่
@water_intake_bp.route('/water-intake', methods=['GET'])  # เปลี่ยนเป็น GET
@token_required
def get_water_intake_by_date(user_id):
    try:
        # ดึงข้อมูลวันที่จาก body
        data = request.args  # ใช้ args เพื่อรับค่าจาก URL query
        date = data.get('date')

        if not date:
            return jsonify({"message": "Please provide a date in the query parameter"}), 400

        # แปลงวันที่ให้เป็น datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()

        # ค้นหาข้อมูลในวันที่ที่ระบุ
        water_record = WaterIntake.query.filter(
            db.func.date(WaterIntake.created_at) == date_obj,
            WaterIntake.user_id == user_id
        ).first()

        # หากไม่มีข้อมูล ให้ตั้งค่า water_amount = 0
        if not water_record:
            result = {
                'water_intake_id': None,
                'user_id': user_id,
                'water_amount': 0,  # ค่าเริ่มต้น
                'created_at': date_obj.strftime('%Y-%m-%d')
            }
        else:
            result = {
                'water_intake_id': water_record.water_intake_id,
                'user_id': water_record.user_id,
                'water_amount': water_record.water_amount,
                'created_at': water_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


# POST: เพิ่มข้อมูลน้ำที่ดื่ม
@water_intake_bp.route('/water-intake', methods=['POST'])
@token_required
def add_water_intake(user_id):
    try:
        data = request.json
        water_amount = data.get('water_amount')

        if not water_amount:
            return jsonify({"message": "Please provide water_amount"}), 400

        # เพิ่มข้อมูลใหม่
        new_record = WaterIntake(
            user_id=user_id,
            water_amount=water_amount
        )

        db.session.add(new_record)
        db.session.commit()

        # ส่งข้อมูลที่บันทึกใหม่กลับ
        return jsonify({
            "message": "Water intake record added successfully!",
            "water_intake_id": new_record.water_intake_id,
            "water_amount": new_record.water_amount,
            "created_at": new_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 201

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


# PUT: อัปเดตข้อมูลน้ำที่ดื่มตาม ID
@water_intake_bp.route('/water-intake/<int:water_intake_id>', methods=['PUT'])
@token_required
def update_water_intake(user_id, water_intake_id):
    try:
        data = request.json
        water_amount = data.get('water_amount')

        if not water_amount:
            return jsonify({"message": "Please provide water_amount"}), 400

        # ค้นหา record ที่ต้องการอัปเดต
        record = WaterIntake.query.filter_by(water_intake_id=water_intake_id, user_id=user_id).first()

        if not record:
            return jsonify({"message": "Water intake record not found."}), 404

        # อัปเดตข้อมูล
        record.water_amount = water_amount
        db.session.commit()

        # ส่งข้อมูลที่อัปเดตกลับ
        return jsonify({
            "message": "Water intake record updated successfully!",
            "water_intake_id": record.water_intake_id,
            "water_amount": record.water_amount,
            "created_at": record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
