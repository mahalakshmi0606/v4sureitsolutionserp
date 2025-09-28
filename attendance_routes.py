from flask import Blueprint, request, jsonify
from app import db
from app.models.attendance import Attendance, current_time_ist
from datetime import datetime, time
import pytz

attendance_bp = Blueprint('attendance', __name__)

# Function to get today's date range in IST
def get_today_range_ist():
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.now(ist)
    today_start = datetime.combine(now_ist.date(), time.min).astimezone(ist)
    today_end = datetime.combine(now_ist.date(), time.max).astimezone(ist)
    return today_start, today_end

@attendance_bp.route('/', methods=['GET'])
def get_today_attendance():
    """
    Get today's attendance for a given user in IST.
    """
    user_id = request.args.get('user_id')
    if not user_id and request.is_json:
        user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    today_start, today_end = get_today_range_ist()

    records = Attendance.query.filter(
        Attendance.user_id == user_id,
        Attendance.timestamp >= today_start,
        Attendance.timestamp <= today_end
    ).order_by(Attendance.timestamp.asc()).all()

    result = [
        {
            'id': r.id,
            'username': r.username,
            'user_id': r.user_id,
            'action': r.action,
            'timestamp': r.timestamp.isoformat(),
            'note': r.note or ''
        } for r in records
    ]

    return jsonify(result)

@attendance_bp.route('/', methods=['POST'])
def submit_attendance():
    """
    Submit a new attendance entry.
    Validates actions to ensure logical flow.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    username = data.get('username')
    user_type = data.get('user_type')
    action = data.get('action')
    note = data.get('note', '')

    if not all([user_id, username, user_type, action]):
        return jsonify({'error': 'user_id, username, user_type, and action are required'}), 400

    today_start, today_end = get_today_range_ist()

    todays_entries = Attendance.query.filter(
        Attendance.user_id == user_id,
        Attendance.timestamp >= today_start,
        Attendance.timestamp <= today_end
    ).all()

    actions_today = [entry.action for entry in todays_entries]

    if action == "In Office":
        if "In Office" in actions_today:
            return jsonify({'error': 'Already marked In Office today.'}), 400
        if "Work From Home" in actions_today:
            return jsonify({'error': 'Cannot mark In Office if Work From Home is already marked today.'}), 400

    elif action == "Work From Home":
        if "Work From Home" in actions_today:
            return jsonify({'error': 'Already marked Work From Home today.'}), 400
        if "In Office" in actions_today:
            return jsonify({'error': 'Cannot mark Work From Home if In Office is already marked today.'}), 400

    elif action == "Leaving Office":
        if "Leaving Office" in actions_today:
            return jsonify({'error': 'Already marked Leaving Office today.'}), 400
        if "In Office" not in actions_today:
            return jsonify({'error': 'Cannot mark Leaving Office without marking In Office first.'}), 400

    # Create and save attendance
    new_attendance = Attendance(
        user_id=user_id,
        username=username,
        user_type=user_type,
        action=action,
        note=note,
        timestamp=current_time_ist()  # Save as IST
    )

    db.session.add(new_attendance)
    db.session.commit()

    return jsonify({'message': 'Attendance recorded successfully.'})

@attendance_bp.route('/history', methods=['GET'])
def attendance_history():
    """
    Return full attendance history for a given user.
    """
    user_id = request.args.get('user_id')
    if not user_id and request.is_json:
        user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    records = Attendance.query.filter_by(user_id=user_id).order_by(Attendance.timestamp.desc()).all()

    return jsonify([
        {
            'id': r.id,
            'username': r.username,
            'user_id': r.user_id,
            'action': r.action,
            'timestamp': r.timestamp.isoformat(),
            'note': r.note or ''
        } for r in records
    ])
