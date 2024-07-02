from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy() #instancia para gestión de la DB
login = LoginManager() #instancia para gestión de sesión

def create_app():
    
    app = Flask(__name__, template_folder='../templates', static_folder="../static") #rutas del templates y static
    csrf = CSRFProtect(app) #protector CSRF para evitar peticiones maliciosas 
    
    app.config.from_object(Config) #conexión con la DB y la llave secreta

    db.init_app(app) #inicializa la DB
    login.init_app(app) # inicializa la gestión de sesión
    login.login_view = 'main.login'  # Ruta para la página de inicio de sesión

    from app import models  # Importar modelos para registrar las tablas

    @login.user_loader #decorador para cargar usuario
    def load_user(user_id):
        return models.Usuarios.query.get(int(user_id))

    with app.app_context(): # itera el archivo models y crea todas las tablas en la base de datos
        db.create_all()

    from app.routes import main  # Importar el Blueprint
    app.register_blueprint(main)

    return app