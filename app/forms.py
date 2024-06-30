from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(), Email()])  # Campo para el email con validación de datos requeridos y formato de email
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])  # Campo para la contraseña con validación de datos requeridos y longitud mínima/máxima
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])  # Campo para confirmar la contraseña, debe coincidir con el campo de contraseña
  nombre = StringField('Nombre')  # Campo para el nombre con validación de datos requeridos
  submit = SubmitField('Register')  # Botón de envío del formulario

class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired(), Email()])  # Campo para el email con validación de datos requeridos y formato de email
  password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])  # Campo para la contraseña con validación de datos requeridos
  remember = BooleanField('Remember Me')  # Campo opcional para recordar la sesión del usuario
  submit = SubmitField('Login')  # Botón de envío del formulario

class PublicacionForm(FlaskForm):
    contenido = TextAreaField('¿Qué estás pensando?', validators=[DataRequired()])
    submit = SubmitField('Publicar')

class ComentarioForm(FlaskForm):
    contenido = TextAreaField('Comentario', validators=[DataRequired()])
    submit = SubmitField('Comentar')