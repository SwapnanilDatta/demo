import os
from flask import Flask
from dotenv import load_dotenv

from extensions import socketio
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.analytics import analytics_bp
from routes.views import views_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_fallback_secret_key')

    # Initialize extensions
    socketio.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(views_bp)

    return app

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)