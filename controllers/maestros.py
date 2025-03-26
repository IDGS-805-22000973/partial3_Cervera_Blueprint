from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.models import db, Maestros, Grupos, Alumnos, Preguntas, RespuestasAlumnos
from werkzeug.security import generate_password_hash
import forms
from controllers.auth import maestro_required

maestros_bp = Blueprint('maestros', __name__)

@maestros_bp.route("/Maestro1", methods=['GET', 'POST'])
def Maestro1():
    create_form = forms.UserForm3(request.form)

    if request.method == 'POST':
        hashed_pw = generate_password_hash(create_form.password.data)
        maestro = Maestros(
            nombre=create_form.nombre.data,
            apellido_paterno=create_form.apellido_paterno.data,
            apellido_materno=create_form.apellido_materno.data,
            email=create_form.email.data,
            password=hashed_pw
        )
        db.session.add(maestro)
        db.session.commit()
        return redirect(url_for('maestros.Maestro1'))
    
    return render_template("Maestro1.html", form=create_form)

@maestros_bp.route("/Alumnos1", methods=['GET', 'POST'])
@maestro_required
def Alumnos1():
    create_form = forms.UserForm2(request.form)
    grupos = Grupos.query.all()
    
    if request.method == 'POST':
        hashed_pw = generate_password_hash(create_form.password.data)
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apellido_paterno=create_form.apellido_paterno.data,
            apellido_materno=create_form.apellido_materno.data,
            fecha_nacimiento=create_form.fecha_nacimiento.data,
            grupo_id=create_form.grupo_id.data,
            email=create_form.email.data,
            password=hashed_pw
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('maestros.Alumnos1'))

    return render_template("Alumnos1.html", form=create_form, grupos=grupos)

@maestros_bp.route("/agregar_pregunta", methods=['GET', 'POST'])
@maestro_required
def agregar_pregunta():
    create_form = forms.PreguntaForm(request.form)
    
    if request.method == 'POST':
        pregunta = Preguntas(
            texto=create_form.texto.data,
            respuesta_a=create_form.respuesta_a.data,
            respuesta_b=create_form.respuesta_b.data,
            respuesta_c=create_form.respuesta_c.data,
            respuesta_d=create_form.respuesta_d.data,
            respuesta_correcta=create_form.respuesta_correcta.data
        )
        db.session.add(pregunta)
        db.session.commit()
        flash("Pregunta agregada exitosamente", "success")
        return redirect(url_for('maestros.agregar_pregunta'))
    
    return render_template("agregar_pregunta.html", form=create_form)

@maestros_bp.route('/grupos')
@maestro_required
def grupos():
    grupos = Grupos.query.all() 
    grupo_id = request.args.get('grupo_id')
    grupo_seleccionado = None
    alumnos = []

    if grupo_id:
        grupo_seleccionado = Grupos.query.get(grupo_id)
        alumnos = Alumnos.query.filter_by(grupo_id=grupo_id).all()

    return render_template('grupos.html', grupos=grupos, grupo_seleccionado=grupo_seleccionado, alumnos=alumnos)