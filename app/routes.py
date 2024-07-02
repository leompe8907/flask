from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import RegistrationForm, LoginForm, PublicacionForm, ComentarioForm
from app.models import Usuarios, Publicaciones
from sqlalchemy.orm import session

main = Blueprint('main', __name__) #organizar las rutas para que se puedan utilizar en el init

# Se crea una instancia con el formulario del registro, se valida que el email ingresado no este ya en la DB, de ser asi te regresa un mensaje de error, si el correo es nuevo guarda los datos en la DB y te redirige al login
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if Usuarios.query.filter_by(email=form.email.data).first():
            flash('Correo Existente', 'danger')
            return redirect(url_for('main.register'))
        user = Usuarios(email=form.email.data, nombre=form.nombre.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Felicidades, te has registrado', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


#si el usuario ya esta autenticado te redirige al home sino te hace sa solicitud del correo y la contraseña la valida y despues te redirige al home, en caso que no coincidan los datos no te dejara avanzar
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Email o Contraseña incorrecta', 'danger')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember.data)
        flash('Inicio de Sesión Exitosa ', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    return render_template('login.html', form=form)


#elimina la sesión
@main.route('/logout')
def logout():
    logout_user()
    flash('Te has deslogueado exitosamente.', 'success')
    return redirect(url_for('main.index'))


#se crea una instancia del formulario de publicidad y si el usuario esta autenticado te permite crear una publicación y la almacena en la DB con el id del que la creo, nombre, texto, tipo, fecha
@main.route('/', methods=['GET', 'POST'])
def index():
    form = PublicacionForm()
    if current_user.is_authenticated and form.validate_on_submit():
        publicacion = Publicaciones(contenido=form.contenido.data, autor=current_user, tipo='publicacion')
        db.session.add(publicacion)
        db.session.commit()
        flash('Tu publicación ha sido creada!', 'success')
        return redirect(url_for('main.index'))
    publicaciones = Publicaciones.query.filter_by(tipo='publicacion').order_by(Publicaciones.date.desc()).all()
    return render_template('index.html', form=form, publicaciones=publicaciones)


# se crea una instancia en el formulario de comentario y si se envia la información en el formulario de forma correcta, se realiza la solicitud post para crear la publicidad tipo comentario
@main.route('/comentar/<int:publicacion_id>', methods=['POST'])
@login_required
def comentar(publicacion_id):
    form = ComentarioForm()
    if form.validate_on_submit():
        comentario = Publicaciones(contenido=form.contenido.data, autor=current_user, tipo='comentario', publicacion_id=publicacion_id)
        db.session.add(comentario)
        db.session.commit()
        return jsonify({"success": "Tu comentario ha sido publicado"}), 200
    return jsonify({"error": "Error al validar el formulario"}), 400


#se obtiene el id de la publicidad, después se iteran en la tabla de publicidades hasta encontrar el id para eliminarlos y también a todos los comentarios que tengan relación con este id
@main.route('/eliminar/<int:id>', methods=['DELETE'])
@login_required
def eliminar_publicacion(id):
    publicacion = Publicaciones.query.get_or_404(id)
    if current_user.id != publicacion.autor_id:
        return jsonify({'error': 'No tienes permiso para eliminar esta publicación.'}), 403
    
    try:
        with db.session.no_autoflush:
            # Eliminar todos los comentarios asociados a la publicación
            if publicacion.tipo == 'publicacion':
                for comentario in publicacion.comentarios:
                    db.session.delete(comentario)
            
            db.session.delete(publicacion)
            db.session.commit()
            return jsonify({'success': 'Tu publicación ha sido eliminada!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar la publicación: {}'.format(str(e))}), 500

# se obtiene el id de la publicidad y después se verifica si la persona logueada es el mismo que creo la publicidad de serlo se habilitara la opción de poder editarla atravez de un método PUT
@main.route('/editar/<int:id>', methods=['GET', 'PUT'])
@login_required
def editar_publicacion(id):
    publicacion = Publicaciones.query.get_or_404(id)
    if current_user.id != publicacion.autor_id:
        flash('No tienes permiso para editar esta publicación.', 'danger')
        return redirect(url_for('main.index'))
    
    form = PublicacionForm()
    if request.method == 'PUT' and form.validate_on_submit():
        publicacion.contenido = form.contenido.data
        db.session.commit()
        return jsonify({'success': 'Tu publicación ha sido actualizada!'}), 200
    elif request.method == 'GET':
        form.contenido.data = publicacion.contenido
    return render_template('editar_publicacion.html', form=form, publicacion=publicacion)


