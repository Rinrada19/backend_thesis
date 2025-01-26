from db import db

class Meal(db.Model):
    __tablename__ = 'meal'


    meal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ใช้ autoincrement สำหรับ meal_id
    food_name = db.Column(db.String, nullable=False)  # ชื่ออาหาร (ต้องระบุ)
    food_description = db.Column(db.String, nullable=True)  # รายละเอียดอาหาร (ไม่จำเป็นต้องระบุ)
    type = db.Column(db.String, nullable=False)  # ประเภทอาหาร (ต้องระบุ)
    rice = db.Column(db.Integer, nullable=True)  # ปริมาณข้าว (สามารถเว้นว่างได้)
    egg = db.Column(db.String, nullable=True)  # ประเภทไข่ (สามารถเว้นว่างได้)
    meal_type = db.Column(db.String, nullable=True)  # ประเภทมื้ออาหาร (สามารถเว้นว่างได้)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())  # เวลาเริ่มต้น (ค่าเริ่มต้นเป็นเวลาปัจจุบัน)
    cal = db.Column(db.Integer, nullable=False, default=0)  # แคลอรี่ (ค่าเริ่มต้น 0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # เชื่อมกับตาราง users (สามารถเว้นว่างได้)
    fat = db.Column(db.Float, nullable=False, default=0.0)  # ไขมัน (ค่าเริ่มต้น 0.0)
    carb = db.Column(db.Float, nullable=False, default=0.0)  # คาร์โบไฮเดรต (ค่าเริ่มต้น 0.0)
    protein = db.Column(db.Float, nullable=False, default=0.0)  # โปรตีน (ค่าเริ่มต้น 0.0)
    sugar = db.Column(db.Float, nullable=False, default=0.0)  # น้ำตาล (ค่าเริ่มต้น 0.0)
    sodium = db.Column(db.Float, nullable=False, default=0.0)  # โซเดียม (ค่าเริ่มต้น 0.0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # แก้ไขตรงนี้

    def __repr__(self):
        return f"<Meal {self.food_name} (ID: {self.meal_id})>"

