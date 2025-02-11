from inference_sdk import InferenceHTTPClient
import requests

# ตั้งค่า API URL
API_URL = "http://98.82.34.52:5000/predict"

def analyze_image(image_path):
    try:
        # เปิดไฟล์ภาพและส่งไปยัง API
        with open(image_path, "rb") as image_file:
            files = {"file": image_file}  # อัปโหลดไฟล์แบบ multipart/form-data
            response = requests.post(API_URL, files=files)

        # ตรวจสอบว่า API ตอบกลับสำเร็จหรือไม่
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            return []

        result = response.json()  # แปลงผลลัพธ์เป็น JSON
        print(f"Result from API: {result}")  # Debug ผลลัพธ์จาก API

        # ตรวจสอบว่า API ตอบกลับ `predictions`
        if 'predictions' in result and isinstance(result['predictions'], list):
            predictions = result['predictions']
        else:
            predictions = []

        if predictions:
            food_classes = [prediction['class'] for prediction in predictions]  # รายการ class
            food_confidences = [prediction['confidence'] for prediction in predictions]  # ความมั่นใจ
            food_coordinates = [prediction['coordinates'] for prediction in predictions]  # พิกัด
            
            # แสดงผลลัพธ์
            print(f"Food Classes: {food_classes}")
            print(f"Food Confidences: {food_confidences}")
            print(f"Food Coordinates: {food_coordinates}")

            return food_classes  # คืนค่าเฉพาะรายการ class ของอาหาร
        else:
            print("ไม่มีเมนูนี้")  # ถ้าไม่มีข้อมูลที่ตรวจพบ
            return []
    
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return []  # ส่งค่าเป็น list ว่างหากเกิดข้อผิดพลาด



# from inference_sdk import InferenceHTTPClient
# import base64

# CLIENT = InferenceHTTPClient(
#    # api_url="https://detect.roboflow.com",
#     api_url="http://98.82.34.52:5000/predict",
#     api_key="Kn94QmbZA9QnSOOs4ZgA"
# )

# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         # อ่านไฟล์ภาพและแปลงเป็น base64
#         encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#     return encoded_string

# def analyze_image(image_path):
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
#             food_ids = [prediction.get('class') for prediction in predictions]  # ดึง 'class' ทุกตัว
#             print(f"Food IDs: {food_ids}")  # แสดงรายการ food_id
#             return food_ids  # คืนค่าทั้งหมดของ food_ids
#         else:
#             print("ไม่มีเมนูนี้")  # เปลี่ยนเป็นข้อความที่ต้องการ
#             return "ไม่มีเมนูนี้"  # คืนค่าข้อความ "ไม่มีเมนูนี้" แทนการคืนลิสต์ว่าง
#     except Exception as e:
#         print(f"Error analyzing image: {e}")
#         return "เกิดข้อผิดพลาดในการวิเคราะห์ภาพ"  # ส่งข้อความข้อผิดพลาดหากเกิดข้อผิดพลาด
