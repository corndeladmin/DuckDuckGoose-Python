from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class HonkForm(FlaskForm):
    content = TextAreaField(label='Write your honk', validators=[DataRequired(), Length(max=255)])
    submit = SubmitField(label='Honk')
