# Smart Task Management System

A Flask-based task management web application that utilizes PostgreSQL for data persistence, Pandas & NumPy for real-time analytics, and Flask-SocketIO for instant WebSocket updates.
## 🎥 Project Demo

https://github.com/SwapnanilDatta/demo/blob/main/Recording.mp4

## Features
- **User Authentication:** Register and login securely using Werkzeug hashing and Flask sessions.
- **Task Management:** Full CRUD (Create, Read, Update, Delete) for your personal tasks.
- **Analytics Dashboard:** Live analytics powered by Pandas and NumPy calculate your total tasks, pending count, completed count, and completion percentage.
- **Real-Time UI:** Flask-SocketIO pushes real-time events to the frontend, updating the dashboard across all your active browser tabs instantly when a task is updated.
- **Modular Architecture:** The codebase is split into Flask Blueprints for clean routing and easy maintainability.

## Project Structure
```text
.
├── app.py                 # Main application entry point
├── db.py                  # Database connection helper
├── extensions.py          # Flask extensions (SocketIO)
├── init_db.py             # Script to initialize the database
├── routes/                # Flask Blueprints
│   ├── analytics.py       # Pandas/NumPy endpoints
│   ├── auth.py            # Registration & Login endpoints
│   ├── tasks.py           # Task CRUD endpoints
│   └── views.py           # HTML rendering endpoints
├── static/
│   └── style.css          # Vanilla CSS styling
├── templates/             # HTML templates (base, index, login, register)
├── schema.sql             # PostgreSQL tables schema
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not tracked in git)
```

## Setup & Run Instructions

### 1. Database Setup
You need a running PostgreSQL database (e.g., via [Render](https://render.com) or local installation).
Create a `.env` file in the root directory containing your **External Database URL**:
```ini
DATABASE_URL=postgresql://username:password@host/dbname
SECRET_KEY=your_random_secret_key
```

### 2. Environment
Create and activate a Python virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Initialize Tables
Run the initialization script to automatically create your `users` and `tasks` tables:
```bash
python init_db.py
```

### 4. Run the Server
Start the Flask application using Socket.IO:
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your web browser.
