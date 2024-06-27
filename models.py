from extensions import db
from datetime import datetime

class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(20), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

class Publicaciones(db.Model):
    __tablename__ = "publicaciones"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    autor = db.relationship('Usuarios', backref='publicaciones')