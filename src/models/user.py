from flask_login import UserMixin

from src.db import db, bcrypt


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    hashed_password = db.Column(db.String(length=255), nullable=False)

    @property
    def password(self):
        raise AttributeError('Plaintext password not available')

    @password.setter
    def password(self, plaintext_password):
        self.hashed_password = bcrypt.generate_password_hash(plaintext_password).decode()

    def password_matches(self, plaintext_password):
        return bcrypt.check_password_hash(self.hashed_password, plaintext_password)
