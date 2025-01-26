from db import db

class FriendInfo(db.Model):
    __tablename__ = 'friend_info'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    friend_username = db.Column(db.String, nullable=False)
    friend_calories = db.Column(db.String, nullable=False)
    caloric_intake_id = db.Column(db.Integer, nullable=False)
    meal_eaten_id = db.Column(db.Integer, nullable=False)
    friend_caloric_intake_id = db.Column(db.Integer, db.ForeignKey('caloric_intake.caloric_intake_id', ondelete='CASCADE', onupdate='NO ACTION'), nullable=True)

    def __repr__(self):
        return (f"<FriendInfo UserID: {self.user_id}, FriendID: {self.friend_id}, "
                f"Username: {self.friend_username}, Calories: {self.friend_calories}>")
