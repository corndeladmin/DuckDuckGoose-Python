from datetime import datetime

from src.db import db
from .user import User


class Honk(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id), nullable=False)
    user = db.relationship('User', backref=db.backref('honks', lazy='dynamic'))
    content = db.Column(db.String(length=255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
