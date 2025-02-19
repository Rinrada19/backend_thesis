from flask import Blueprint, jsonify

def create_food_bp():
    from app import db  # นำเข้า db ที่นี่ในฟังก์ชัน
    from models.food import Food  # นำเข้าโมเดล Food ที่นี่ในฟังก์ชัน
    
    food_bp = Blueprint('food', __name__)

    @food_bp.route('/foods', methods=['GET'])
    def get_foods():
        foods = Food.query.all()
        result = [
            {
                'food_id': food.food_id,
                'food_name': food.food_name,
                'food_description': food.food_description,
                'fat': food.fat,
                'carb': food.carb,
                'protein': food.protein,
                'cal': food.cal,
                'sugar': food.suger,  # เปลี่ยนชื่อฟิลด์เป็น sugar
                'sodium': food.sodium,
                'ingredient': food.ingredient,
                #'image': food.image,
                'default_meat': food.default_meat,
                'food_category': food.food_category

            }
            for food in foods
        ]
        return jsonify(result)
    
    @food_bp.route('/foods/<int:item_id>', methods=['GET'])  
    def get_food_by_id(item_id):
        try:
            food = Food.query.get(item_id)  # ค้นหาด้วย item_id
            if not food:
                return jsonify({"message": "Food item not found"}), 404

            return jsonify({             
                'food_id': food.food_id,
                'food_name': food.food_name,
                'food_description': food.food_description,
                'fat': food.fat,
                'carb': food.carb,
                'protein': food.protein,
                'cal': food.cal,
                'sugar': food.suger,  # เปลี่ยนชื่อฟิลด์เป็น sugar
                'sodium': food.sodium,
                'ingredient': food.ingredient,
               # 'image': food.image,
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return food_bp
