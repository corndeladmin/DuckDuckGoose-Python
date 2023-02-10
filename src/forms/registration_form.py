from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Length, EqualTo

from re import fullmatch

from src.models.user import User


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField(label='Password', widget=PasswordInput(hide_value=False), validators=[DataRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField(label='Confirm password', widget=PasswordInput(hide_value=False), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label='Register')

    def validate_username(form, field):
        if not fullmatch('[a-z0-9_]+', field.data):
            raise ValidationError('Usernames can only contain lowercase letters, numbers and underscores.')
        user_with_same_username = User.query.filter_by(username=field.data).first()
        if user_with_same_username:
            raise ValidationError('That username is already taken.')
