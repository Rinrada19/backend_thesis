from app import db
from datetime import datetime

class WaterIntake(db.Model):
    __tablename__ = 'water_intake'

    water_intake_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)  # Foreign Key
    water_amount = db.Column(db.Float, nullable=False)  # ปริมาณน้ำที่ดื่ม
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # วันที่สร้างข้อมูล

    # ความสัมพันธ์กับโมเดล User (ถ้าจำเป็น)
    user = db.relationship('User', backref=db.backref('water_intakes', lazy=True))

    def __init__(self, user_id, water_amount):
        self.user_id = user_id
        self.water_amount = water_amount

