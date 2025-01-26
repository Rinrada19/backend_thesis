from datetime import datetime
from app import db  # หรือจากที่ที่คุณนำเข้า db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ใช้ 'user_id' เป็น primary key

    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    dietary_restriction = db.Column(db.ARRAY(db.String), default=[])  # เปลี่ยนเป็น ARRAY
    congenital_disease = db.Column(db.ARRAY(db.String), default=[])  # เปลี่ยนเป็น ARRAY
    
    physical_activity = db.Column(db.String(50), nullable=True)
    goal = db.Column(db.String(100), nullable=True)
    require_weight = db.Column(db.Float, nullable=True)
    bmi = db.Column(db.Float, nullable=True)
    goal_cal = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # เพิ่มแอตทริบิวต์นี้
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # เพิ่มแอตทริบิวต์นี้

    meals = db.relationship('Meal', backref='user', lazy=True)  # ความสัมพันธ์กับตารางอื่น

    def __repr__(self):
        return f'<User {self.username}>'
