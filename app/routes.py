from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import db, login
from app import login
from app.forms import RegistrationForm, LoginForm, PublicacionForm, ComentarioForm
from app.models import Usuarios, Publicaciones, Comentarios

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if Usuarios.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('main.register'))
        user = Usuarios(email=form.email.data, nombre=form.nombre.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

login = LoginManager()

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember.data)
        flash('Login successful!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PublicacionForm()
    if current_user.is_authenticated and form.validate_on_submit():
        publicacion = Publicaciones(contenido=form.contenido.data, autor=current_user)
        db.session.add(publicacion)
        db.session.commit()
        flash('Tu publicación ha sido creada!', 'success')
        return redirect(url_for('main.index'))
    publicaciones = Publicaciones.query.order_by(Publicaciones.date.desc()).all()
    return render_template('index.html', form=form, publicaciones=publicaciones)

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_publicacion(id):
    publicacion = Publicaciones.query.get_or_404(id)
    if current_user.id != publicacion.autor_id:
        flash('No tienes permiso para editar esta publicación.', 'danger')
        return redirect(url_for('main.index'))
    form = PublicacionForm()
    if form.validate_on_submit():
        publicacion.contenido = form.contenido.data
        db.session.commit()
        flash('Tu publicación ha sido actualizada!', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.contenido.data = publicacion.contenido
    return render_template('editar_publicacion.html', form=form)

@main.route('/eliminar/<int:id>')
@login_required
def eliminar_publicacion(id):
    publicacion = Publicaciones.query.get_or_404(id)
    if current_user.id != publicacion.autor_id:
        flash('No tienes permiso para eliminar esta publicación.', 'danger')
        return redirect(url_for('main.index'))
    db.session.delete(publicacion)
    db.session.commit()
    flash('Tu publicación ha sido eliminada!', 'success')
    return redirect(url_for('main.index'))