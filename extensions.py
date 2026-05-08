from flask_socketio import SocketIO

# Initialize socketio without app. We'll init_app later in app.py
socketio = SocketIO(cors_allowed_origins="*")
