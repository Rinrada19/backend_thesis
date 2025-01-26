from flask_sqlalchemy import SQLAlchemy
from db import db

class CaloricIntake(db.Model):
    __tablename__ = 'caloric_intake'

    caloric_intake_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    cal_goal = db.Column(db.Float, nullable=False)
    total_cal = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carb = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    water = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=False)
    meal_eaten_id = db.Column(db.Integer, db.ForeignKey('meal_eaten.meal_eaten_id'), nullable=False)
    fat_goal = db.Column(db.Float)
    carb_goal = db.Column(db.Float)
    protein_goal = db.Column(db.Float)
    sugar_goal = db.Column(db.Float)
    sodium_goal = db.Column(db.Float)
    sodium = db.Column(db.Float, default=0)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_id_date'),
    )

    def __init__(self, user_id, date, cal_goal, total_cal, fat, carb, protein, water, sugar, meal_eaten_id):
        self.user_id = user_id
        self.date = date
        self.cal_goal = cal_goal
        self.total_cal = total_cal
        self.fat = fat
        self.carb = carb
        self.protein = protein
        self.water = water
        self.sugar = sugar
        self.meal_eaten_id = meal_eaten_id
