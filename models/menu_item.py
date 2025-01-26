from db import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import CheckConstraint, ForeignKey

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ใช้ primary key item_id
    item_name = db.Column(db.String(255), nullable=False)  # ชื่ออาหาร
    item_description = db.Column(db.Text, nullable=True)  # คำอธิบายอาหาร
    food_category =db.Column(db.String, nullable=True) # หมวดหมู่อาหาร
    calories = db.Column(db.Numeric, nullable=True)  # แคลอรี่
    fat = db.Column(db.Numeric, nullable=True)  # ไขมัน
    carbs = db.Column(db.Numeric, nullable=True)  # คาร์โบไฮเดรต
    protein = db.Column(db.Numeric, nullable=True)  # โปรตีน
    sugar = db.Column(db.Numeric, nullable=True)  # น้ำตาล
    sodium = db.Column(db.Numeric, nullable=True)  # โซเดียม
    ingredients = db.Column(db.String, nullable=True)  # เก็บเป็น string แทน array
    image = db.Column(db.String(255), nullable=True)  # URL รูปภาพ
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())  # วันที่สร้าง
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())   # วันที่อัปเดตล่าสุด
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)  # แก้ไขตรงนี้

    # ใช้ __table_args__ สำหรับข้อกำหนดเพิ่มเติม
    __table_args__ = (
        CheckConstraint(
            "food_category IN ('อาหาร', 'เครื่องดื่ม', 'ของหวาน')",
            name='menu_items_food_category_check'
        ),
    )
