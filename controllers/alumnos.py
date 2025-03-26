from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from models.models import db, Alumnos, Preguntas, RespuestasAlumnos
import forms
from controllers.auth import alumno_required

alumnos_bp = Blueprint('alumnos', __name__)

def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

@alumnos_bp.route('/examen', methods=['GET', 'POST'])
@alumno_required
def examen():
    alumno_id = session['user_id']
    alumno = Alumnos.query.get(alumno_id)
    edad = calcular_edad(alumno.fecha_nacimiento)
    preguntas = Preguntas.query.all()
    
    form = forms.EmptyForm()
    
    return render_template('examen.html', 
                         alumno=alumno, 
                         edad=edad, 
                         preguntas=preguntas,
                         form=form)

@alumnos_bp.route('/guardar_examen', methods=['POST'])
@alumno_required
def guardar_examen():
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        alumno = Alumnos.query.get(alumno_id)
        total_preguntas = 0
        respuestas_correctas = 0

        for pregunta in Preguntas.query.all():
            respuesta_elegida = request.form.get(f'pregunta_{pregunta.id}')

            if respuesta_elegida:
                nueva_respuesta = RespuestasAlumnos(
                    alumno_id=alumno_id,
                    pregunta_id=pregunta.id,
                    respuesta_elegida=respuesta_elegida
                )
                db.session.add(nueva_respuesta)

                if respuesta_elegida == pregunta.respuesta_correcta:
                    respuestas_correctas += 1
                
                total_preguntas += 1

        calificacion = (respuestas_correctas / total_preguntas) * 10 if total_preguntas > 0 else 0
        alumno.calificacion = calificacion
        db.session.commit()
    flash("Examen enviado correctamente", "success")
    return redirect(url_for('alumnos.examen'))