from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.models.user import db, User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError

users_bp = Blueprint('users_routes', __name__, url_prefix='/api/users')

# Sample data
DEPARTMENTS = [
    {"dept_id": 1, "dept_name": "IT"},
    {"dept_id": 2, "dept_name": "HR"},
    {"dept_id": 3, "dept_name": "Finance"}
]

USER_TYPES = [
    {"type": "super_admin", "label": "Super Admin"},
    {"type": "admin", "label": "Admin"},
    {"type": "user", "label": "Regular User"}
]

@users_bp.route('/', methods=['GET'])
@cross_origin()
def get_all_users():
    users = User.query.all()
    return jsonify([{
        "user_id": u.user_id,
        "user_name": u.user_name,
        "user_type": u.user_type,
        "email_id": u.email_id,
        "departments": u.departments,
        "phone_no": u.phone_no,
        "status": u.status,
        "created_by": u.created_by,
        "created_on": u.created_on.isoformat() if u.created_on else None
    } for u in users]), 200

@users_bp.route('', methods=['POST'])
@cross_origin()
def add_user():
    data = request.get_json()
    required_fields = ['user_name', 'user_password', 'user_type', 'email_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    if User.query.filter_by(email_id=data['email_id']).first():
        return jsonify({"error": "Email already registered"}), 400

    new_user = User(
        user_name=data['user_name'],
        user_password=generate_password_hash(data['user_password']),
        user_type=data['user_type'],
        email_id=data['email_id'],
        departments=data.get('departments', ''),
        phone_no=data.get('phone_no', ''),
        status=data.get('status', '1'),
        created_by=data.get('created_by', 'System'),
        created_on=datetime.utcnow()
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {
            "user_id": new_user.user_id,
            "user_name": new_user.user_name,
            "email_id": new_user.email_id
        }
    }), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
@cross_origin()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if 'user_name' in data:
        user.user_name = data['user_name']

    if 'email_id' in data:
        if User.query.filter(User.email_id == data['email_id'], User.user_id != user_id).first():
            return jsonify({"error": "Email already in use"}), 400
        user.email_id = data['email_id']

    if 'user_type' in data:
        user.user_type = data['user_type']

    if 'phone_no' in data:
        user.phone_no = data['phone_no']

    if 'status' in data:
        user.status = data['status']

    if 'departments' in data:
        user.departments = data['departments']

    if 'user_password' in data and data['user_password']:
        user.user_password = generate_password_hash(data['user_password'])

    db.session.commit()

    return jsonify({
        "message": "User updated",
        "user": {
            "user_id": user.user_id,
            "user_name": user.user_name
        }
    }), 200

@users_bp.route('/<int:user_id>', methods=['DELETE'], strict_slashes=False)
@cross_origin()
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        inspector = inspect(user)
        for relationship in inspector.mapper.relationships:
            if getattr(user, relationship.key):
                return jsonify({
                    "error": "User has associated records",
                    "relationship": relationship.key
                }), 422

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "message": "User deleted",
            "deleted_user_id": user_id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Deletion failed",
            "details": str(e)
        }), 500

@users_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    email = data.get('email_id') or data.get('email')
    password = data.get('user_password') or data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email_id=email).first()
    if not user or not check_password_hash(user.user_password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "user_type": user.user_type,
            "email_id": user.email_id
        }
    }), 200

@users_bp.route('/me', methods=['GET'])
@cross_origin()
def get_me():
    # If you're not using JWT, you may need to pass user ID from frontend explicitly
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "user_name": user.user_name,
        "email_id": user.email_id,
        "user_type": user.user_type
    }), 200

@users_bp.route('/usertypes', methods=['GET'])
@cross_origin()
def get_user_types():
    return jsonify(USER_TYPES), 200

@users_bp.route('/departments', methods=['GET'])
@cross_origin()
def get_departments():
    return jsonify(DEPARTMENTS), 200
