from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import Maestros, Alumnos
from werkzeug.security import check_password_hash
import forms
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    
    if request.method == 'POST' and login_form.validate():
        email = login_form.email.data
        password = login_form.password.data
        
        # Verificar si es maestro
        maestro = Maestros.query.filter_by(email=email).first()
        if maestro and check_password_hash(maestro.password, password):
            session['user_id'] = maestro.id
            session['user_type'] = 'maestro'
            session['nombre'] = f"{maestro.nombre} {maestro.apellido_paterno}"
            return redirect(url_for('maestros.Maestro1'))
        
        # Verificar si es alumno
        alumno = Alumnos.query.filter_by(email=email).first()
        if alumno and check_password_hash(alumno.password, password):
            session['user_id'] = alumno.id
            session['user_type'] = 'alumno'
            session['nombre'] = f"{alumno.nombre} {alumno.apellido_paterno}"
            return redirect(url_for('alumnos.examen'))
        
        flash("Email o contraseña incorrectos", "danger")
    
    return render_template("login.html", form=login_form)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route("/")
def index():
    if 'user_id' in session:
        if session['user_type'] == 'maestro':
            return render_template('index_maestro.html')
        else:
            return redirect(url_for('alumnos.examen'))
    return redirect(url_for('auth.login'))

# Decorador para verificar que el usuario es maestro
def maestro_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'maestro':
            flash("Acceso restringido a maestros", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar que el usuario es alumno
def alumno_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_type' not in session or session['user_type'] != 'alumno':
            flash("Acceso restringido a alumnos", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function