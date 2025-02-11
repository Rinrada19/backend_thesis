import os

# class Config:
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost/postgres')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # ค่าคีย์ที่ใช้ในการเข้ารหัส
#     LOGIN_VIEW = 'users.login'
    
    
    
    
    
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres1234@lkakaloly.cjq0eaqisx5g.ap-southeast-2.rds.amazonaws.com:5432/Kakaloly')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # ค่าคีย์ที่ใช้ในการเข้ารหัส
    LOGIN_VIEW = 'users.login'