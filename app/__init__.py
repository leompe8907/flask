from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder="../static")
    csrf = CSRFProtect(app)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    login.login_view = 'main.login'  # Ruta para la página de inicio de sesión

    from app import models  # Importar modelos para registrar las tablas

    @login.user_loader
    def load_user(user_id):
        return models.Usuarios.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    from app.routes import main  # Importar el Blueprint
    app.register_blueprint(main)

    return app