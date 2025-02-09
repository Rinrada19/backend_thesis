# from flask import request, jsonify
# import base64
# # from inference_http_client import InferenceHTTPClient
# from inference_sdk import InferenceHTTPClient

# # ตั้งค่าตัวแปร CLIENT สำหรับเชื่อมต่อกับ API
# CLIENT = InferenceHTTPClient(
#     api_url="http://98.82.34.52:5000/predict",
#     api_key="Kn94QmbZA9QnSOOs4ZgA"
# )

# def image_to_base64(image_path):
#     # ฟังก์ชันแปลงภาพเป็น base64
#     with open(image_path, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#     return encoded_string

# def analyze_image(image_path):
#     food_id = request.args.get('food_id')  # รับค่าจาก query string หรืออื่นๆ

#     # ตรวจสอบว่า food_id มีค่าหรือไม่
#     if food_id is None:
#         return jsonify({"message": "food_id is required."}), 400

#     # ตรวจสอบว่า food_id เป็นตัวเลขหรือไม่
#     try:
#         food_id = int(food_id)  # แปลงให้เป็นจำนวนเต็ม
#     except ValueError:
#         return jsonify({"message": "Invalid food_id, must be a number."}), 400

#     try:
#         # แปลงภาพเป็น base64
#         base64_image = image_to_base64(image_path)

#         # ส่งคำขอไปยัง API พร้อมกับ base64 image
#         result = CLIENT.infer(base64_image, model_id="thai-food-detection-xvc0m/3")

#         # แสดงผลลัพธ์ที่ได้รับจาก API
#         print(f"Result from API: {result}")  # ตรวจสอบว่าผลลัพธ์จาก API เป็นอย่างไร
        
#         # ตรวจสอบว่า 'predictions' มีข้อมูลหรือไม่
#         if 'predictions' in result:
#             predictions = result['predictions']
#         else:
#             predictions = []
        
#         if predictions:
#             # ดึง 'class' ทุกตัวจากผลลัพธ์
#             food_ids = [prediction.get('class') for prediction in predictions]  
#             print(f"Food IDs: {food_ids}")  # แสดงรายการ food_id
#             return jsonify({"food_ids": food_ids}), 200  # คืนค่าผลลัพธ์ที่ได้รับจาก API
#         else:
#             print("ไม่มีเมนูนี้")  # ถ้าไม่มีการทำนาย
#             return jsonify({"message": "No menu detected."}), 404  # คืนค่าข้อความ "ไม่มีเมนูนี้"
#     except Exception as e:
#         print(f"Error analyzing image: {e}")
#         return jsonify({"message": "Error analyzing image."}), 500  # ส่งข้อความข้อผิดพลาดหากเกิดข้อผิดพลาด


from inference_sdk import InferenceHTTPClient
import base64

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Kn94QmbZA9QnSOOs4ZgA"
)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # อ่านไฟล์ภาพและแปลงเป็น base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def analyze_image(image_path):
    try:
        # แปลงภาพเป็น base64
        base64_image = image_to_base64(image_path)

        # ส่งคำขอไปยัง API พร้อมกับ base64 image
        result = CLIENT.infer(base64_image, model_id="thai-food-detection-xvc0m/3")
        
        # แสดงผลลัพธ์ที่ได้รับจาก API
        print(f"Result from API: {result}")  # ตรวจสอบว่าผลลัพธ์จาก API เป็นอย่างไร
        
        # ตรวจสอบว่า 'predictions' มีข้อมูลหรือไม่
        if 'predictions' in result:
            predictions = result['predictions']
        else:
            predictions = []
        
        if predictions:
            food_ids = [prediction.get('class') for prediction in predictions]  # ดึง 'class' ทุกตัว
            print(f"Food IDs: {food_ids}")  # แสดงรายการ food_id
            return food_ids  # คืนค่าทั้งหมดของ food_ids
        else:
            print("ไม่มีเมนูนี้")  # เปลี่ยนเป็นข้อความที่ต้องการ
            return "ไม่มีเมนูนี้"  # คืนค่าข้อความ "ไม่มีเมนูนี้" แทนการคืนลิสต์ว่าง
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return "เกิดข้อผิดพลาดในการวิเคราะห์ภาพ"  # ส่งข้อความข้อผิดพลาดหากเกิดข้อผิดพลาด
