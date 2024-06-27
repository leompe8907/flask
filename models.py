from app import db
from datetime import datetime

class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID de usuario, clave primaria, autoincrementable
    email = db.Column(db.String(80), nullable=False, unique=True)  # Email del usuario, debe ser único y no nulo
    password = db.Column(db.String(200), nullable=False)  # Contraseña del usuario, no nula
    nombre = db.Column(db.String(50), nullable=False)  # Nombre del usuario, no nulo
    created = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación, con valor por defecto la fecha y hora actual

class Publicaciones(db.Model):
    __tablename__ = "publicaciones"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID de la publicación, clave primaria, autoincrementable
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID del autor, clave foránea referenciando a usuarios.id
    autor = db.relationship('Usuarios', backref='publicaciones')  # Relación con la tabla Usuarios, con backref a publicaciones
    titulo = db.Column(db.String(200), nullable=False)  # Título de la publicación, no nulo
    contenido = db.Column(db.Text, nullable=False)  # Contenido de la publicación, no nulo
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de la publicación, con valor por defecto la fecha y hora actual

class Comentarios(db.Model):
    __tablename__ = "comentarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID del comentario, clave primaria, autoincrementable
    publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones.id'), nullable=False)  # ID de la publicación, clave foránea referenciando a publicaciones.id
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID del autor del comentario, clave foránea referenciando a usuarios.id
    contenido = db.Column(db.Text, nullable=False)  # Contenido del comentario, no nulo
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha del comentario, con valor por defecto la fecha y hora actual
    publicacion = db.relationship('Publicaciones', backref='comentarios')  # Relación con la tabla Publicaciones, con backref a comentarios
    autor = db.relationship('Usuarios', backref='comentarios')  # Relación con la tabla Usuarios, con backref a comentarios
