from db import db

class SavedMeal(db.Model):
    __tablename__ = 'saved_meal'

    saved_meal_id = db.Column(db.Integer, primary_key=True)  # ให้ฐานข้อมูลสร้างค่า auto-increment
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.meal_id'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False)

