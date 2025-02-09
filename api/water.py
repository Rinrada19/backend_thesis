from flask import Blueprint, request, jsonify
from app import db
from models.water import WaterIntake
import datetime
from services.auth_service import token_required

# สร้าง Blueprint
water_intake_bp = Blueprint('water_intake', __name__)

# GET: ดึงข้อมูลน้ำที่ดื่มตามวันที่
@water_intake_bp.route('/water-intake', methods=['GET'])
@token_required
def get_water_intake_by_date(user_id):
    try:
        # ดึงข้อมูลวันที่จาก query parameters
        data = request.args
        date = data.get('date')

        if not date:
            return jsonify({"message": "Please provide a date in the query parameter"}), 400

        # แปลงวันที่ให้เป็น datetime object
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()

        # ค้นหาข้อมูลในวันที่ที่ระบุ และดึงเฉพาะข้อมูลที่มี created_at ล่าสุด
        water_record = WaterIntake.query.filter(
            db.func.date(WaterIntake.created_at) == date_obj,
            WaterIntake.user_id == user_id
        ).order_by(WaterIntake.created_at.desc()).first()  # ใช้ .first() เพื่อดึงเฉพาะตัวล่าสุด

        if not water_record:
            return jsonify({"message": "No water intake records found for the given date"}), 201

        # ส่งข้อมูลที่ค้นหาได้
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

        # หาข้อมูลบันทึกน้ำดื่มล่าสุดที่ถูกบันทึกในวันนี้
        today = datetime.date.today()  # ใช้ datetime.date.today() แทน datetime.datetime.now().date()
        existing_record = WaterIntake.query.filter(
            WaterIntake.user_id == user_id,
            db.func.date(WaterIntake.created_at) == today
        ).first()

        if existing_record:
            # ถ้ามีข้อมูลแล้ว ให้ทำการอัปเดต
            existing_record.water_amount = water_amount
            db.session.commit()

            return jsonify({
                "message": "Water intake record updated successfully!",
                "water_intake_id": existing_record.water_intake_id,
                "water_amount": existing_record.water_amount,
                "created_at": existing_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }), 200
        else:
            # ถ้าไม่มีข้อมูลในวันนี้ ให้เพิ่มข้อมูลใหม่
            new_record = WaterIntake(
                user_id=user_id,
                water_amount=water_amount
            )
            db.session.add(new_record)
            db.session.commit()

            return jsonify({
                "message": "Water intake record added successfully!",
                "water_intake_id": new_record.water_intake_id,
                "water_amount": new_record.water_amount,
                "created_at": new_record.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }), 201

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

# PUT: อัปเดตข้อมูลน้ำที่ดื่มตาม ID
@water_intake_bp.route('/water-intake', methods=['PUT'])
@token_required
def update_water_intake(user_id):
    try:
        data = request.json
        water_amount = data.get('water_amount')

        if water_amount is None:
            return jsonify({"message": "Missing water_amount"}), 400

        # หาวันปัจจุบัน (หรือใช้ค่าที่ส่งมา)
        today = datetime.datetime.now().date()
        existing_record = WaterIntake.query.filter(
            db.func.date(WaterIntake.created_at) == today,
            WaterIntake.user_id == user_id
        ).first()

        if existing_record:
            # ถ้ามีข้อมูลแล้ว → อัปเดต
            existing_record.water_amount = water_amount
            db.session.commit()
            return jsonify({"message": "Water intake updated", "data": existing_record.to_dict()}), 200
        else:
            # ถ้ายังไม่มีข้อมูล → สร้างใหม่
            new_record = WaterIntake(
                user_id=user_id,
                water_amount=water_amount,
                created_at=datetime.datetime.now()
            )
            db.session.add(new_record)
            db.session.commit()
            return jsonify({"message": "Water intake created", "data": new_record.to_dict()}), 201

    except Exception as e:
        print("Error updating water intake:", str(e))
        return jsonify({"message": "Internal Server Error"}), 500
