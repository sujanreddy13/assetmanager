from flask import Flask
from config import Config
from extensions import db, jwt
from routes.auth_routes import auth_bp
from routes.asset_routes import asset_bp
from routes.employee_routes import employee_bp

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def home():
        return "Asset Manager API is running!"
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(asset_bp)
    app.register_blueprint(employee_bp)

    with app.app_context():
        db.create_all()

    return app
