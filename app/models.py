from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

class Publicaciones(db.Model):
    __tablename__ = "publicaciones_comentarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    autor = db.relationship('Usuarios', backref='publicaciones_comentarios')
    tipo = db.Column(db.String(50), nullable=False)  # 'publicacion' o 'comentario'
    contenido = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones_comentarios.id'), nullable=True)  # Solo para comentarios
    comentarios = db.relationship('Publicaciones', backref=db.backref('publicacion', remote_side=[id]), cascade="all, delete-orphan")
