from flask import Blueprint, request, jsonify
from db import db
from models.friend import Friend
from services.auth_service import token_required

friend_bp = Blueprint('friend', __name__)  # ไม่มี url_prefix

@friend_bp.route('/friend', methods=['GET'])
@token_required
def get_friends(user_id):
    # ค้นหาความสัมพันธ์เพื่อนทั้งสองฝั่ง
    friends = Friend.query.filter(
        (Friend.user_id == user_id) 
    ).all()

    return jsonify([{
        "user_id": friend.user_id,
        "friend_id": friend.friend_id,
        "added_at": friend.added_at
    } for friend in friends]), 200


from datetime import datetime

@friend_bp.route('/friend', methods=['POST'])
@token_required
def create_friend(user_id):
    data = request.json
    friend_id = data.get('friend_id')

    if not friend_id:
        return jsonify({"error": "friend_id is required"}), 400

    # ตรวจสอบก่อนว่ามีข้อมูลเพื่อนนี้อยู่แล้วหรือไม่
    existing_friend1 = Friend.query.filter(
        (Friend.user_id == user_id) & (Friend.friend_id == friend_id)
    ).first()

    existing_friend2 = Friend.query.filter(
        (Friend.user_id == friend_id) & (Friend.friend_id == user_id)
    ).first()

    if existing_friend1 or existing_friend2:
        return jsonify({"error": "Friendship already exists"}), 400

    try:
        # เพิ่มเพื่อนในทั้งสองฝั่ง
        new_friend1 = Friend(
            user_id=user_id,
            friend_id=friend_id,
            added_at=datetime.utcnow()
        )

        new_friend2 = Friend(
            user_id=friend_id,
            friend_id=user_id,
            added_at=datetime.utcnow()
        )

        db.session.add(new_friend1)
        db.session.add(new_friend2)  # เพิ่มความสัมพันธ์ในฝั่งตรงข้าม
        db.session.commit()
        return jsonify({"message": "Friend added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@friend_bp.route('/friend', methods=['DELETE'])
@token_required
def delete_friend(user_id):
    data = request.get_json()  # รับข้อมูลจาก body
    friend_id = data.get('friend_id')  # ดึง friend_id จาก body

    if not friend_id:
        return jsonify({"error": "friend_id is required"}), 400

    try:
        # ค้นหาข้อมูลเพื่อนในทั้งสองฝั่ง (user_id, friend_id) และ (friend_id, user_id)
        friend1 = Friend.query.filter_by(user_id=user_id, friend_id=friend_id).first()
        friend2 = Friend.query.filter_by(user_id=friend_id, friend_id=user_id).first()

        # หากเจอข้อมูลเพื่อนในฝั่งที่กำหนด ให้ลบทั้งสองฝั่ง
        if friend1:
            db.session.delete(friend1)
        if friend2:
            db.session.delete(friend2)

        db.session.commit()
        return jsonify({"message": "Friend deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
