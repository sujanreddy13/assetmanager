from flask import Flask
from config import Config
from extensions import db, jwt, scheduler
from routes.auth_routes import auth_bp
from routes.asset_routes import asset_bp
from routes.employee_routes import employee_bp
from routes.filter_routes import filter_bp
from tasks.asset_tasks import asset_return_reminder  

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Asset Manager API is running!"

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    scheduler.init_app(app)

    if not scheduler.get_job("asset_return_reminder"):
        scheduler.add_job(
            id="asset_return_reminder",
            func=asset_return_reminder,
            trigger="interval",
            minutes=1,
            args=[app]  
        )
    scheduler.start()
    app.register_blueprint(auth_bp)
    app.register_blueprint(asset_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(filter_bp)

    with app.app_context():
        db.create_all()

    return app
