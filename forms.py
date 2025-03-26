from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms import StringField,IntegerField
from wtforms import EmailField
from wtforms import validators
from wtforms import StringField, PasswordField, SelectField, DateField, FloatField
from wtforms.validators import DataRequired, Email
 
 
class UserForm(Form):
    nombre=StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=10, message='ingresa nombre valido')
    ])
    apaterno=StringField('apaterno')
    amaterno=StringField('amaterno')
    email=EmailField('email',[ validators.Email(message='Ingrese un correo valido')])
    edad=IntegerField('edad')
 
 
class UserForm2(Form):
    id=IntegerField('id',
    [validators.number_range(min=1, max=20,message='valor no valido')])
    
    nombre=StringField('Nombre:',[
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4,max=20, message='requiere min=4 max=20')
    ])
   
    apellido_paterno=StringField('Apellido Paterno:',[
        validators.DataRequired(message='El apellido es requerido')
    ])

    apellido_materno=StringField('Apellido Materno:',[
        validators.DataRequired(message='El apellido es requerido')
    ])

    email=StringField('Email:',[
        validators.DataRequired(message='El email es requerido')
    ])
   
    password=PasswordField('Contraseña:',[
        validators.DataRequired(message='La contraseña es requerida')
    ])

    fecha_nacimiento=StringField('Fecha de nacimiento:',[

    ])

    grupo_id=StringField('Grupo:',[

    ])


class UserForm3(Form):
    id=IntegerField('id',
    [validators.number_range(min=1, max=20,message='valor no valido')])
    
    nombre=StringField('Nombre:',[
        validators.DataRequired(message='El nombre es requerido'),
        validators.length(min=4,max=20, message='requiere min=4 max=20')
    ])
   
    apellido_paterno=StringField('Apellido Paterno:',[
        validators.DataRequired(message='El apellido es requerido')
    ])

    apellido_materno=StringField('Apellido Materno:',[
        validators.DataRequired(message='El apellido es requerido')
    ])

    email=StringField('Email:',[
        validators.DataRequired(message='El email es requerido')
    ])
   
    password=PasswordField('Contraseña:',[
        validators.DataRequired(message='La contraseña es requerida')
    ])


class PreguntaForm(Form):
    texto = StringField("Pregunta:", validators=[DataRequired()])
    respuesta_a = StringField("Opción A:", validators=[DataRequired()])
    respuesta_b = StringField("Opción B:", validators=[DataRequired()])
    respuesta_c = StringField("Opción C:", validators=[DataRequired()])
    respuesta_d = StringField("Opción D:", validators=[DataRequired()])
    respuesta_correcta = SelectField(
        "Respuesta Correcta:",
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        validators=[DataRequired()]
    )
    submit = SubmitField("Agregar Pregunta")


class BuscarAlumnoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(message='Ingrese nombre')])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(message='Ingrese apellido paterno')])
    submit = SubmitField('Buscar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Ingrese el email'), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Ingrese la contraseña')])

class EmptyForm(FlaskForm):
    # Formulario vacío solo para el token CSRF
    pass