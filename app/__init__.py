from flask import Flask
from flask_cors import CORS
from .extensions import db, bcrypt
from .config import Config


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5000"]}},
         supports_credentials=True)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    from .controllers.recipe_controller import recipe_blueprint
    app.register_blueprint(recipe_blueprint, url_prefix='/recipes')

    from .controllers.user_controller import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
