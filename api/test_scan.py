from inference_sdk import InferenceHTTPClient

# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="http://98.82.34.52:5000/predict",
    api_key="Kn94QmbZA9QnSOOs4ZgA"
)

# ระบุพาธไฟล์รูปภาพที่ต้องการทำนาย
IMAGE_PATH = "D:/code/2024/Thesis/backend/api/test.jpg"  # เปลี่ยนให้เป็นพาธที่ถูกต้อง

# infer on a local image
result = CLIENT.infer(IMAGE_PATH, model_id="thai-food-detection-xvc0m/3")

# แสดงผลลัพธ์ที่ได้
print("📊 ผลลัพธ์จาก API:", result)
