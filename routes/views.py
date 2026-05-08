from flask import Blueprint, render_template, session, redirect, url_for

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('views.login_page'))
    return render_template('index.html', username=session.get('username'))

@views_bp.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('views.index'))
    return render_template('login.html')

@views_bp.route('/register')
def register_page():
    if 'user_id' in session:
        return redirect(url_for('views.index'))
    return render_template('register.html')
