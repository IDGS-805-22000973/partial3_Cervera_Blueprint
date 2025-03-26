from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Grupos(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    alumnos = db.relationship('Alumnos', back_populates='grupo')


class Maestros(db.Model):
    __tablename__ = 'maestros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Guardar contraseñas hasheadas en producción

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    calificacion = db.Column(db.Float, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Nuevo campo para login
    password = db.Column(db.String(255), nullable=False)  # Nuevo campo para login

    grupo = db.relationship('Grupos', back_populates='alumnos')
    respuestas = db.relationship('RespuestasAlumnos', back_populates='alumno')

    def calcular_edad(self):
        today = datetime.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

class Preguntas(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(255), nullable=False)
    respuesta_a = db.Column(db.String(255), nullable=False)
    respuesta_b = db.Column(db.String(255), nullable=False)
    respuesta_c = db.Column(db.String(255), nullable=False)
    respuesta_d = db.Column(db.String(255), nullable=False)
    respuesta_correcta = db.Column(db.String(255), nullable=False)

    respuestas_alumnos = db.relationship('RespuestasAlumnos', back_populates='pregunta')

class RespuestasAlumnos(db.Model):
    __tablename__ = 'respuestas_alumnos'
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
    respuesta_elegida = db.Column(db.String(255), nullable=False)
    
    alumno = db.relationship('Alumnos', back_populates='respuestas')
    pregunta = db.relationship('Preguntas', back_populates='respuestas_alumnos')