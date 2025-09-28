# app/routes/admin_attendance.py
from flask import Blueprint, request, jsonify
from app import db
from app.models.attendance import Attendance
from app.models.user import User
from sqlalchemy import and_, func
from datetime import datetime

admin_attendance_bp = Blueprint('admin_attendance_bp', __name__, url_prefix='/api/admin')

@admin_attendance_bp.route('/attendance', methods=['GET'])
def get_all_attendance():
    try:
        department = request.args.get('department')
        user_type = request.args.get('user_type')
        date = request.args.get('date')  # YYYY-MM-DD

        # Build the base query with join
        query = db.session.query(Attendance, User).join(User, Attendance.user_id == User.user_id)

        if department:
            query = query.filter(User.departments == department)
        if user_type:
            query = query.filter(User.user_type == user_type)
        if date:
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(func.date(Attendance.timestamp) == date_obj)
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        results = query.order_by(Attendance.timestamp.desc()).all()

        data = []
        for attendance, user in results:
            data.append({
                "attendance_id": attendance.id,
                "user_id": user.user_id,
                "user_name": user.user_name,
                "user_type": user.user_type,
                "department": user.departments,
                "attendance_status": attendance.action,
                "attendance_date": attendance.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "note": attendance.note or ''
            })

        return jsonify(data), 200

    except Exception as e:
        print("Admin Attendance Error:", str(e))
        return jsonify({"error": "Something went wrong"}), 500
