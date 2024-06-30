from flask import Flask
from config import Config
from app.extensions import db

def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        from app import models  # Importar modelos para registrar las tablas
        db.create_all()

    from app.routes import main  # Importar el Blueprint
    app.register_blueprint(main)

    return app
