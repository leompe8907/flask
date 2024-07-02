import sys
import os

# Añade la ruta de tu aplicación
path = '/home/leonard27/my_flask_app'
if path not in sys.path:
    sys.path.append(path)

# Establece la variable de entorno para la configuración de Flask
os.environ['FLASK_APP'] = 'app'

from app import app as application
