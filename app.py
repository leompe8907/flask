from flask import Flask
from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    with app.app_context():
        from models import Usuarios, Publicaciones
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)