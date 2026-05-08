from flask import Blueprint, request, jsonify, session
from psycopg2.extras import RealDictCursor
from db import get_db_connection
from extensions import socketio

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM tasks WHERE user_id = %s ORDER BY created_date DESC;",
            (session['user_id'],)
        )
        tasks = cur.fetchall()
        return jsonify({"status": "success", "data": tasks}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@tasks_bp.route('', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    priority = data.get('priority', 'Medium')
    status = data.get('status', 'Pending')
    
    if not title:
        return jsonify({"status": "error", "message": "Title is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tasks (user_id, title, description, priority, status)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (session['user_id'], title, description, priority, status))
        new_id = cur.fetchone()[0]
        conn.commit()
        
        socketio.emit('task_updated', {'message': 'A new task was added', 'user_id': session['user_id']})
        
        return jsonify({"status": "success", "task_id": new_id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority')
    status = data.get('status')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM tasks WHERE id = %s AND user_id = %s;", (task_id, session['user_id']))
        if not cur.fetchone():
            return jsonify({"status": "error", "message": "Task not found or unauthorized"}), 404

        cur.execute("""
            UPDATE tasks SET title = %s, description = %s, priority = %s, status = %s
            WHERE id = %s AND user_id = %s;
        """, (title, description, priority, status, task_id, session['user_id']))
        conn.commit()
        
        socketio.emit('task_updated', {'message': 'Task was updated', 'user_id': session['user_id']})
        return jsonify({"status": "success", "message": "Task updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s RETURNING id;", (task_id, session['user_id']))
        deleted = cur.fetchone()
        conn.commit()
        
        if not deleted:
            return jsonify({"status": "error", "message": "Task not found"}), 404
            
        socketio.emit('task_updated', {'message': 'Task was deleted', 'user_id': session['user_id']})
        return jsonify({"status": "success", "message": "Task deleted"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()
