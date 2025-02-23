from db import db
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # รหัสเมนู
    food_name = db.Column(db.String(255), nullable=False)  # ชื่ออาหาร
    food_description = db.Column(db.Text, nullable=True)  # คำอธิบายอาหาร
    food_category = db.Column(db.String, nullable=True)  # หมวดหมู่อาหาร
    cal = db.Column(db.Numeric, nullable=True)  # แคลอรี่
    fat = db.Column(db.Numeric, nullable=True)  # ไขมัน
    carb = db.Column(db.Numeric, nullable=True)  # คาร์โบไฮเดรต
    protein = db.Column(db.Numeric, nullable=True)  # โปรตีน
    sugar = db.Column(db.Numeric, nullable=True)  # น้ำตาล
    sodium = db.Column(db.Numeric, nullable=True)  # โซเดียม
    ingredient = db.Column(db.String, nullable=True)  # ส่วนผสม (เก็บเป็น string แทน array)
    default_meat = db.Column(db.String(255), nullable=True)  # เนื้อสัตว์เริ่มต้น
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())  # วันที่สร้าง
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())  # วันที่อัปเดตล่าสุด
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), nullable=False)  # ผู้ใช้ที่เพิ่มเมนู

    # ใช้ __table_args__ สำหรับข้อกำหนดเพิ่มเติม
    __table_args__ = (
        CheckConstraint(
            "food_category IN ('อาหาร', 'เครื่องดื่ม', 'ของหวาน')",
            name='menu_items_food_category_check'
        ),
    )
