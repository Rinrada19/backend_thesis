from flask import Flask
from db import db
from config import Config
from flask_cors import CORS
from flask_mail import Mail
import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
   
    # ตั้งค่าต่าง ๆ
    app.config.from_object(Config)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = 'ftlz vghz ysmn qmgh'
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
   # CORS(app, origins="*", supports_credentials=True)
    print("MAIL_PASSWORD:", app.config['MAIL_PASSWORD'])
    CORS(app, origins=["https://kakaloly.vercel.app/", "http://localhost:3000"], supports_credentials=True)

    # เรียกใช้ db.init_app เพื่อเชื่อมต่อกับ Flask app
    db.init_app(app)

    with app.app_context():
        # นำเข้า blueprint สำหรับเส้นทางต่าง ๆ
        from api.food import create_food_bp  
        app.register_blueprint(create_food_bp())

        from api.users import create_users_bp
        app.register_blueprint(create_users_bp(), url_prefix='/users')

        from api.reset_pass import reset_pass_bp
        app.register_blueprint(reset_pass_bp)
        
        from api.meal import create_meal_bp  
        app.register_blueprint(create_meal_bp())
        
        from api.meal_eaten import meal_eaten_bp
        app.register_blueprint(meal_eaten_bp, url_prefix='/meal_eaten')

        from api.caloric_intake import caloric_intake_bp
        app.register_blueprint(caloric_intake_bp)
        
        from api.caloric_intake_new import eat_today_bp 
        app.register_blueprint(eat_today_bp)

        from api.water import water_intake_bp
        app.register_blueprint(water_intake_bp)

        from api.upload_image import create_upload_image_bp
        app.register_blueprint(create_upload_image_bp())

        from api.menu_item import menu_item_api  # นำเข้า Blueprint
        app.register_blueprint(menu_item_api)

        from api.friend import friend_bp  # นำเข้า Blueprint
        app.register_blueprint(friend_bp)  # ไม่ต้องใส่ url_prefix

        from api.saved_meal import saved_meal_bp
        app.register_blueprint(saved_meal_bp)
    
        from api.friend_info import friendinfo_bp  
        app.register_blueprint(friendinfo_bp)
        # สร้างตารางในฐานข้อมูล (ควรใช้ในระหว่างการพัฒนา หรือเมื่อจำเป็น)
        db.create_all()

    return app

# สร้างและรัน Flask app
app = create_app()
mail = Mail(app)
load_dotenv()  
if __name__ == '__main__':
    # รันเซิร์ฟเวอร์ให้สามารถเข้าถึงได้จากทุก IP (0.0.0.0) และกำหนดพอร์ตเป็น 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
