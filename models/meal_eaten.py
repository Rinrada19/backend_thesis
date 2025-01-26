from db import db

class MealEaten(db.Model):
    __tablename__ = 'meal_eaten'

    meal_eaten_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False, default=db.func.now())
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.meal_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    # Relationship with Meal
    meal = db.relationship('Meal', backref=db.backref('meal_eaten', lazy=True))

    def __repr__(self):
        return f"<MealEaten (ID: {self.meal_eaten_id}, Meal ID: {self.meal_id}, User ID: {self.user_id})>"
