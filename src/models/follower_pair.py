from src.db import db
from .user import User


class FollowerPair(db.Model):
    followed_user_id = db.Column(db.Integer(), db.ForeignKey(User.id), primary_key=True)
    followed_user = db.relationship('User', foreign_keys=[followed_user_id], backref=db.backref('follower_users', lazy='dynamic'))
    follower_user_id = db.Column(db.Integer(), db.ForeignKey(User.id), primary_key=True)
    follower_user = db.relationship('User', foreign_keys=[follower_user_id], backref=db.backref('followed_users', lazy='dynamic'))

    __table_args__ = (
        db.CheckConstraint("followed_user_id != follower_user_id"),
    )
