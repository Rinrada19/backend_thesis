from db import db

class Friend(db.Model):
    __tablename__ = 'friend'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    added_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Friend UserID: {self.user_id}, FriendID: {self.friend_id}, AddedAt: {self.added_at}>"


