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
