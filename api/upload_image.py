import os
from flask import Blueprint, request, jsonify
from api.scan import analyze_image
from models.food import Food
from db import db

def create_upload_image_bp():
    upload_image_bp = Blueprint('upload_image', __name__)

    @upload_image_bp.route('/upload-image', methods=['POST'])
    def upload_image():
        if 'image' not in request.files:
            return jsonify({"error": "No image part"}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # เรียกใช้ฟังก์ชัน analyze_image เพื่อวิเคราะห์ภาพ
        food_classes = analyze_image(file_path)

        if not food_classes:
            return jsonify({"message": "ไม่มีเมนูนี้"})


        results = []
        for food_class in food_classes:
            food = Food.query.filter_by(food_id=food_class).first()
            if food:
                results.append({
                    'food_id': food.food_id,
                    'food_name': food.food_name,
                    'food_description': food.food_description,
                    'fat': food.fat,
                    'carb': food.carb,
                    'protein': food.protein,
                    'cal': food.cal,
                    'sugar': food.suger,  # แก้ไขคำสะกดจาก 'suger' เป็น 'sugar'
                    'sodium': food.sodium,
                    'ingredient': food.ingredient,
                    'image': food.image,
                })

        return jsonify(results)


    return upload_image_bp
