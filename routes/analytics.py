from flask import Blueprint, jsonify, session
import pandas as pd
import numpy as np
from db import get_db_connection

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('', methods=['GET'])
def get_analytics():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    try:
        conn = get_db_connection()
        query = f"SELECT * FROM tasks WHERE user_id = {session['user_id']};"
        df = pd.read_sql_query(query, conn)
        
        total_tasks = len(df)
        if total_tasks == 0:
            return jsonify({
                "status": "success",
                "data": {
                    "total": 0,
                    "completed": 0,
                    "pending": 0,
                    "completion_percentage": 0.0
                }
            }), 200

        completed_tasks = int(df[df['status'] == 'Completed'].shape[0])
        pending_tasks = int(total_tasks - completed_tasks)
        
        completion_ratio = np.divide(completed_tasks, total_tasks)
        completion_percentage = float(np.round(completion_ratio * 100, 2))

        return jsonify({
            "status": "success",
            "data": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": pending_tasks,
                "completion_percentage": completion_percentage
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals(): conn.close()
