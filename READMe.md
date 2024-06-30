# Proyecto Flask

Este es un proyecto basado en Flask que permite la creación y gestión de publicaciones y comentarios.

## Requisitos

Para poder ejecutar este proyecto, necesitas tener instalado:

- Python 3.8 o superior
- Flask 2.0 o superior
- Una base de datos (SQLite, PostgreSQL, etc.)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/leompe8907/flask.git

2. Crea un entorno virtual:
    python -m venv env
    source env/bin/activate

3. Instala las dependencias:
    pip install -r requirements.txt

4. Configura la base de datos:
    Configurar el usuario, contraseña y la base de datos en el archivo config.py
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/blogdb'

5. Instala las dependencias:
    pip install -r requirements.txt

6. Ejecutar la app:
    python app.py

Estructura del Proyecto:
* app.py: Archivo principal que inicia la aplicación Flask.
* config.py: Archivo de configuración donde se definen las variables de entorno.
* requirements.txt: Archivo con las dependencias necesarias para el proyecto.
    - app/: Carpeta que contiene el código de la aplicación.
        * __init__.py: Inicializa la aplicación y las extensiones.
        * extensions.py: Configura las extensiones utilizadas (por ejemplo, SQLAlchemy).
        * forms.py: Define los formularios de Flask-WTF.
        * models.py: Define los modelos de base de datos.
        * routes.py: Define las rutas de la aplicación.
    - static/: Carpeta que contiene archivos estáticos como CSS y JavaScript.
        * login.css: Estilos para la página de login.
        * register.css: Estilos para la página de registro.
    - templates/: Carpeta que contiene las plantillas HTML.
        * base.html: Plantilla base para la aplicación.
        * editar_comentario.html: Plantilla para editar comentarios.
        * editar_publicacion.html: Plantilla para editar publicaciones.
        * index.html: Plantilla principal que muestra las publicaciones y comentarios.
        * login.html: Plantilla para la página de login.
        * publicacion.html: Plantilla para mostrar una publicación individual.
        * register.html: Plantilla para la página de registro.

Uso:
La página principal (/) muestra todas las publicaciones y sus respuestas, los usuarios pueden registrarse y loguearse a través de la barra superior. Los usuarios registrados pueden crear, editar y eliminar sus publicaciones, todos los usuarios pueden ver las publicaciones y comentarios, pero solo los usuarios registrados pueden comentar o responder.

Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

