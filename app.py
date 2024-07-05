import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy.orm import session
from datetime import datetime
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/blogdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

main = Blueprint('main', __name__)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login = LoginManager(app)
login.login_view = 'main.login'

class Usuarios(UserMixin, db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

class Publicaciones(db.Model):
    __tablename__ = "publicaciones_comentarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.relationship('Usuarios', backref='publicaciones_comentarios')
    tipo = db.Column(db.String(50), nullable=False)  # 'publicacion' o 'comentario'
    contenido = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones_comentarios.id'), nullable=True)  # Solo para comentarios
    comentarios = db.relationship('Publicaciones', backref=db.backref('publicacion', remote_side=[id]), cascade="all, delete-orphan")

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Campo para el email con validación de datos requeridos y formato de email
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])  # Campo para la contraseña con validación de datos requeridos y longitud mínima/máxima
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  # Campo para confirmar la contraseña, debe coincidir con el campo de contraseña
    nombre = StringField('Nombre')  # Campo para el nombre con validación de datos requeridos
    submit = SubmitField('Register')  # Botón de envío del formulario

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Campo para el email con validación de datos requeridos y formato de email
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])  # Campo para la contraseña con validación de datos requeridos
    remember = BooleanField('Remember Me')  # Campo opcional para recordar la sesión del usuario
    submit = SubmitField('Login')  # Botón de envío del formulario

class PublicacionForm(FlaskForm):
    contenido = TextAreaField('¿Qué estás pensando?', validators=[DataRequired()])
    submit = SubmitField('Publicar')

class ComentarioForm(FlaskForm):
    contenido = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Comentar')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if Usuarios.query.filter_by(email=form.email.data).first():
            flash('Correo Existente', 'danger')
            return redirect(url_for('main.register'))
        user = Usuarios(email=form.email.data, nombre=form.nombre.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicidades, te has registrado', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email o Contraseña incorrecta', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember.data)
        flash('Inicio de Sesión Exitosa ', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('Te has deslogueado exitosamente.', 'success')
    return redirect(url_for('main.index'))

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PublicacionForm()
    if current_user.is_authenticated and form.validate_on_submit():
        publicacion = Publicaciones(contenido=form.contenido.data, autor=current_user, tipo='publicacion')
        db.session.add(publicacion)
        db.session.commit()
        flash('Tu publicación ha sido creada!', 'success')
        return redirect(url_for('main.index'))
    publicaciones = Publicaciones.query.filter_by(tipo='publicacion').order_by(Publicaciones.date.desc()).all()
    return render_template('index.html', form=form, publicaciones=publicaciones)

@main.route('/comentar/<int:publicacion_id>', methods=['POST'])
@login_required
def comentar(publicacion_id):
    form = ComentarioForm()
    if form.validate_on_submit():
        comentario = Publicaciones(contenido=form.contenido.data, autor=current_user, tipo='comentario', publicacion_id=publicacion_id)
        db.session.add(comentario)
        db.session.commit()
        return jsonify({"success": "Tu comentario ha sido publicado"}), 200
    return jsonify({"error": "Error al validar el formulario"}), 400

@main.route('/eliminar/<int:id>', methods=['DELETE'])
@login_required
def eliminar_publicacion(id):
    publicacion = Publicaciones.query.get_or_404(id)
    if current_user.id != publicacion.autor_id:
        return jsonify({'error': 'No tienes permiso para eliminar esta publicación.'}), 403
    
    try:
        with db.session.no_autoflush:
            # Eliminar todos los comentarios asociados a la publicación
            if publicacion.tipo == 'publicacion':
                for comentario in publicacion.comentarios:
                    db.session.delete(comentario)
            
            db.session.delete(publicacion)
            db.session.commit()
            return jsonify({'success': 'Tu publicación ha sido eliminada!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar la publicación: {}'.format(str(e))}), 500

@main.route('/editar/<int:id>', methods=['GET', 'PUT'])
@login_required
def editar_publicacion(id):
    publicacion = Publicaciones.query.get_or_404(id)
    if current_user.id != publicacion.autor_id:
        flash('No tienes permiso para editar esta publicación.', 'danger')
        return redirect(url_for('main.index'))
    
    form = PublicacionForm()
    if request.method == 'PUT' and form.validate_on_submit():
        publicacion.contenido = form.contenido.data
        db.session.commit()
        return jsonify({'success': 'Tu publicación ha sido actualizada!'}), 200
    elif request.method == 'GET':
        form.contenido.data = publicacion.contenido
    return render_template('editar_publicacion.html', form=form, publicacion=publicacion)

if __name__ == '__main__':
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
