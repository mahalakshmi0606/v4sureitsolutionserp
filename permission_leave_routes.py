from flask import Blueprint, request, jsonify, current_app
from app.models.permission_leave import PermissionLeave
from app.models.user import User
from app import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

permission_leave_bp = Blueprint('permission_leave', __name__)

def allowed_file(filename):
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'pdf'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@permission_leave_bp.route('/', methods=['GET'])
def get_all_leaves():
    leaves = PermissionLeave.query.all()
    return jsonify([leave.to_dict() for leave in leaves]), 200

@permission_leave_bp.route('/<int:id>', methods=['GET'])
def get_leave_by_id(id):
    leave = PermissionLeave.query.get_or_404(id)
    return jsonify(leave.to_dict()), 200

@permission_leave_bp.route('/', methods=['POST'])
def create_leave():
    form_data = request.form
    file = request.files.get('mc_file')

    user_id = form_data.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404

    filename = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))

    last_record = PermissionLeave.query.order_by(PermissionLeave.id.desc()).first()
    next_id = (last_record.id + 1) if last_record else 1
    permission_id = f"PERM-{next_id}"

    leave = PermissionLeave(
        permission_id=permission_id,
        user_id=int(user_id),
        leave_type=form_data.get('leave_type', 'permission'),
        permission_type=form_data.get('permission_type'),
        leave_duration=form_data.get('leave_duration'),
        start_time=form_data.get('start_time'),
        end_time=form_data.get('end_time'),
        reason=form_data.get('reason', 'sick'),
        mc_file=filename,
        explanation=form_data.get('explanation'),
        status='pending'  # Default status
    )

    db.session.add(leave)
    db.session.commit()

    return jsonify({
        "message": "Leave/Permission created successfully",
        "permission_id": permission_id,
        "user_name": user.user_name
    }), 201

@permission_leave_bp.route('/<int:id>', methods=['PUT'])
def update_leave(id):
    form_data = request.form
    file = request.files.get('mc_file')
    leave = PermissionLeave.query.get_or_404(id)

    # Handle optional MC file upload
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        leave.mc_file = filename

    # Update leave details
    leave.leave_type = form_data.get('leave_type', leave.leave_type)
    leave.permission_type = form_data.get('permission_type', leave.permission_type)
    leave.leave_duration = form_data.get('leave_duration', leave.leave_duration)
    leave.start_time = form_data.get('start_time', leave.start_time)
    leave.end_time = form_data.get('end_time', leave.end_time)
    leave.reason = form_data.get('reason', leave.reason)
    leave.explanation = form_data.get('explanation', leave.explanation)
    leave.status = form_data.get('status', leave.status)

    # ✅ NEW: Update the action_by field
    leave.action_by = form_data.get('action_by', leave.action_by)

    db.session.commit()

    return jsonify({"message": "Leave/Permission updated successfully"}), 200

@permission_leave_bp.route('/<int:id>', methods=['DELETE'])
def delete_leave(id):
    leave = PermissionLeave.query.get_or_404(id)
    db.session.delete(leave)
    db.session.commit()
    return jsonify({"message": "Leave/Permission deleted successfully"}), 200

@permission_leave_bp.route('/<int:id>/upload-mc', methods=['PUT'])
def upload_mc_file(id):
    leave = PermissionLeave.query.get_or_404(id)
    file = request.files.get('mc_file')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    upload_path = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_path, exist_ok=True)
    file_path = os.path.join(upload_path, filename)
    file.save(file_path)

    leave.mc_file = filename
    db.session.commit()

    return jsonify({
        "message": "MC file uploaded successfully",
        "mc_file": filename
    }), 200
