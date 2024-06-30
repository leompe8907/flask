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
  __tablename__ = "publicaciones"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID de la publicación, clave primaria, autoincrementable
  autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID del autor, clave foránea referenciando a usuarios.id
  autor = db.relationship('Usuarios', backref='publicaciones')  # Relación con la tabla Usuarios, con backref a publicaciones
  titulo = db.Column(db.String(200), nullable=False)  # Título de la publicación, no nulo
  contenido = db.Column(db.Text, nullable=False)  # Contenido de la publicación, no nulo
  date = db.Column(db.DateTime, default=datetime.now())  # Fecha de la publicación, con valor por defecto la fecha y hora actual

class Comentarios(db.Model):
  __tablename__ = "comentarios"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ID del comentario, clave primaria, autoincrementable
  publicacion_id = db.Column(db.Integer, db.ForeignKey('publicaciones.id'), nullable=False)  # ID de la publicación, clave foránea referenciando a publicaciones.id
  autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)  # ID del autor del comentario, clave foránea referenciando a usuarios.id
  contenido = db.Column(db.Text, nullable=False)  # Contenido del comentario, no nulo
  date = db.Column(db.DateTime, default=datetime.now())  # Fecha del comentario, con valor por defecto la fecha y hora actual
  publicacion = db.relationship('Publicaciones', backref='comentarios')  # Relación con la tabla Publicaciones, con backref a comentarios
  autor = db.relationship('Usuarios', backref='comentarios')  # Relación con la tabla Usuarios, con backref a comentarios
