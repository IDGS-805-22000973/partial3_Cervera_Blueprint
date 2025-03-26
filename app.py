from flask import Flask
from models.config import DevelopmentConfig
from models.models import db
from flask_wtf.csrf import CSRFProtect
from controllers.auth import auth_bp
from controllers.alumnos import alumnos_bp
from controllers.maestros import maestros_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Inicializar extensiones
csrf = CSRFProtect()
csrf.init_app(app)
db.init_app(app)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()