from db import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import CheckConstraint, ForeignKey

class Food(db.Model):
    __tablename__ = 'food'
    
    food_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_name = db.Column(db.String, nullable=False)
    food_description = db.Column(db.String, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carb = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    cal = db.Column(db.Float, nullable=False)
    suger = db.Column(db.Float, nullable=False)  # แก้ชื่อจาก suger เป็น sugar
    sodium = db.Column(db.Float, nullable=False)
    ingredient = db.Column(ARRAY(db.String), nullable=False)  # นำเข้า ARRAY ถูกต้อง
    image = db.Column(db.String, nullable=True)
    default_meat = db.Column(db.String, nullable=False, default='none')
    meat_id = db.Column(db.Integer, ForeignKey('meat_type.meat_id'), nullable=True)
    food_category = db.Column(db.String, nullable=True)
    
    __table_args__ = (
        CheckConstraint(
            "food_category IN ('อาหาร', 'เครื่องดื่ม', 'ของหวาน')",
            name='food_category_check'
        ),
    )
