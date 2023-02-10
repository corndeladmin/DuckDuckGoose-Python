from dotenv import find_dotenv, load_dotenv
import os

from flask import Flask, flash, redirect, url_for, render_template
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from sqlalchemy.exc import IntegrityError

from .helpers.flask_login_extensions import logout_required

from .db import db, bcrypt

from src.forms.honk_form import HonkForm
from src.forms.login_form import LoginForm
from src.forms.registration_form import RegistrationForm

from src.models.user import User
from src.models.honk import Honk

load_dotenv(find_dotenv('.env.development'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI').replace('postgres://', 'postgresql://')

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'
login_manager.login_message = 'Please log in to view this page.'
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/honk', methods=['GET', 'POST'])
@login_required
def honk():
    form = HonkForm()
    if form.validate_on_submit():
        try:
            new_honk = Honk(user_id=current_user.id, content=form.content.data)
            db.session.add(new_honk)
            flash('Honk posted successfully.', 'success')
            return redirect(url_for('honks'))
        except IntegrityError:
            return redirect(url_for('honk'))
    return render_template('honk.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('You have registered successfully.', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_with_same_username = User.query.filter_by(username=form.username.data).first()
        if user_with_same_username and user_with_same_username.password_matches(form.password.data):
            login_user(user_with_same_username)
            flash('You have been logged in successfully.', category='success')
            return redirect(url_for('welcome'))
        else:
            flash('Those credentials aren\'t recognised.', category='danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have been logged out successfully.', category='success')
    return redirect(url_for('welcome'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html')
