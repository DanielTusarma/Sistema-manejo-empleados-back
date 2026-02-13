import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from flask_cors import CORS

from extensions import db, migrate, ma
from api import bp as api_bp
import api.empleados # Importar el módulo para registrar los recursos de empleados
import models # Importar el módulo para registrar los modelos con SQLAlchemy asegurar que estén disponibles para las migraciones


def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos desde variables de entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_AS_ASCII"] = False # Para soportar caracteres UTF-8 en JSON
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    # Habilitar CORS para la API
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprint de la API
    app.register_blueprint(api_bp)
    
    @app.get("/")
    def home():
        return "Api de Empleados"
    
    return app

if __name__ == "__main__":
    app = create_app()

    port = int(os.getenv("PORT", 5000))  # usa 5000 si no existe PORT
    debug_mode = os.getenv("FLASK_ENV") == "development"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )
