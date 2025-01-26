from flask import Blueprint, request, jsonify
from db import db
from models.menu_item import MenuItem  # สมมติว่า Model อยู่ในโฟลเดอร์ models
from services.auth_service import token_required

menu_item_api = Blueprint('menu_item_api', __name__)

# สร้างเมนูใหม่
# สร้างเมนูใหม่
# สร้างเมนูใหม่
@menu_item_api.route('/menu-items', methods=['POST'])
@token_required
def create_menu_item(user_id):
    data = request.json
    try:
        # แปลง ingredients ที่เป็น string เป็น array ของ PostgreSQL
        ingredients = data.get('ingredients', "").split(',')  # ใช้ .split(',') เพื่อแยก string เป็น array

        new_item = MenuItem(
            item_name=data.get('item_name'),
            item_description=data.get('item_description'),
            food_category=data.get('food_category'),
            calories=data.get('calories'),
            fat=data.get('fat'),
            carbs=data.get('carbs'),
            protein=data.get('protein'),
            sugar=data.get('sugar'),
            sodium=data.get('sodium'),
            ingredients=ingredients,  # ส่ง array ที่แยกแล้ว
            image=data.get('image'),
            user_id=user_id  # เพิ่ม user_id ที่ได้จาก token
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Menu item created successfully!", "item_id": new_item.item_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# อ่านข้อมูลเมนูทั้งหมด
@menu_item_api.route('/menu-items', methods=['GET'])
@token_required
def get_all_menu_items(user_id):
    try:
        items = MenuItem.query.filter_by(user_id=user_id).all()  # กรองโดย user_id
        return jsonify([{
            "item_id": item.item_id,
            "item_name": item.item_name,
            "item_description": item.item_description,
            "food_category": item.food_category,
            "calories": item.calories,
            "fat": item.fat,
            "carbs": item.carbs,
            "protein": item.protein,
            "sugar": item.sugar,
            "sodium": item.sodium,
            "ingredients": item.ingredients,
            "image": item.image,
            "user_id": item.user_id
        } for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# อ่านข้อมูลเมนูโดย ID
# อ่านข้อมูลเมนูโดย ID
@menu_item_api.route('/menu-items/<int:item_id>', methods=['GET'])
@token_required
def get_menu_item(user_id, item_id):  # รับ user_id ก่อน item_id
    try:
        item = MenuItem.query.filter_by(item_id=item_id, user_id=user_id).first()
        if not item:
            return jsonify({"message": "Menu item not found"}), 404

        return jsonify({
            "item_id": item.item_id,
            "item_name": item.item_name,
            "item_description": item.item_description,
            "food_category": item.food_category,
            "calories": item.calories,
            "fat": item.fat,
            "carbs": item.carbs,
            "protein": item.protein,
            "sugar": item.sugar,
            "sodium": item.sodium,
            "ingredients": item.ingredients,
            "image": item.image,
            "user_id": item.user_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# อัปเดตเมนูโดย ID
# @menu_item_api.route('/menu-items/<int:item_id>', methods=['PUT'])
# @token_required
# def update_menu_item(item_id, user_id):
#     data = request.json
#     try:
#         item = MenuItem.query.filter_by(item_id=item_id, user_id=user_id).first()
#         if not item:
#             return jsonify({"message": "Menu item not found"}), 404

#         # อัปเดตข้อมูลของเมนู
#         item.item_name = data.get('item_name', item.item_name)
#         item.item_description = data.get('item_description', item.item_description)
#         item.food_category = data.get('food_category', item.food_category)
#         item.calories = data.get('calories', item.calories)
#         item.fat = data.get('fat', item.fat)
#         item.carbs = data.get('carbs', item.carbs)
#         item.protein = data.get('protein', item.protein)
#         item.sugar = data.get('sugar', item.sugar)
#         item.sodium = data.get('sodium', item.sodium)
#         item.ingredients = data.get('ingredients', item.ingredients)
#         item.image = data.get('image', item.image)

#         db.session.commit()
#         return jsonify({"message": "Menu item updated successfully!"}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 400


# ลบเมนูโดย ID
@menu_item_api.route('/menu-items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_menu_item(user_id, item_id):  # รับ user_id ก่อน item_id
    try:
        item = MenuItem.query.filter_by(item_id=item_id, user_id=user_id).first()
        if not item:
            return jsonify({"message": "Menu item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Menu item deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
