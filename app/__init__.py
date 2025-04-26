from flask import Flask
from .routes import main as main_blueprint
from .config import Config
from .models import db
from flask_migrate import Migrate
import atexit
from .deepseek import Deepseek_llm

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Load configuration
    app.config.from_object(Config)
    # Initialize database
    db.init_app(app)
    # Initialize migration
    migrate.init_app(app, db)
    # Register blueprints
    app.register_blueprint(main_blueprint)
    # Create database tables
    with app.app_context():
        db.create_all()


    return app