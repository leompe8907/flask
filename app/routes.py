from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import Usuarios

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuarios(email=form.email.data, nombre=form.nombre.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        flash('Login successful!')
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/')
def index():
    return 'Welcome to the Flask App!'
