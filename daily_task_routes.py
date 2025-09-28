from flask import Blueprint, request, jsonify
from app import db
from app.models.daily_task import DailyTask
from app.models.user import User
from app.models.project import Project
from datetime import datetime

daily_task_bp = Blueprint('daily_task', __name__, url_prefix='/api/daily_task')

@daily_task_bp.route('/', methods=['GET'])
def get_all_daily_tasks():
    tasks = DailyTask.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@daily_task_bp.route('/<int:task_id>', methods=['GET'])
def get_daily_task(task_id):
    task = DailyTask.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@daily_task_bp.route('/', methods=['POST'])
def create_daily_task():
    data = request.get_json()

    try:
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404

        project = Project.query.get(data['project_id'])
        if not project:
            return jsonify({"error": "Project not found"}), 404

        new_task = DailyTask(
            user_id=data['user_id'],
            project_id=data['project_id'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            deadline=datetime.strptime(data['deadline'], '%Y-%m-%d').date(),
            priority=data.get('priority', 'medium'),
            daily_task=data['daily_task'],
            daily_work_hours=data.get('daily_work_hours', 8)
        )

        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Daily task created successfully", "task": new_task.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@daily_task_bp.route('/<int:task_id>', methods=['PUT'])
def update_daily_task(task_id):
    task = DailyTask.query.get_or_404(task_id)
    data = request.get_json()

    try:
        if 'user_id' in data:
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({"error": "User not found"}), 404
            task.user_id = data['user_id']

        if 'project_id' in data:
            project = Project.query.get(data['project_id'])
            if not project:
                return jsonify({"error": "Project not found"}), 404
            task.project_id = data['project_id']

        if 'start_date' in data:
            task.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'deadline' in data:
            task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
        if 'priority' in data:
            task.priority = data['priority']
        if 'daily_task' in data:
            task.daily_task = data['daily_task']
        if 'daily_work_hours' in data:
            task.daily_work_hours = data['daily_work_hours']

        db.session.commit()
        return jsonify({"message": "Daily task updated successfully", "task": task.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@daily_task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_daily_task(task_id):
    task = DailyTask.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Daily task deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
