import secrets
from flask import Flask
from flask_injector import FlaskInjector
from models import db
from routes import api
import views

from infrastructure.container_configurer import configure_container

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sininkii2305200@localhost/db_payment'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    # ✅ Initialize extensions
    db.init_app(app)

    # ✅ Register Routes
    app.register_blueprint(api)

    # ✅ Apply Dependency Injection
    FlaskInjector(app=app, modules=[configure_container])

    return app



