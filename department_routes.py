from flask import Blueprint, request, jsonify
from app.models.department import db, Department
from datetime import datetime

departments_bp = Blueprint('departments', __name__)

# GET all departments or handle OPTIONS request
@departments_bp.route('/', methods=['GET', 'OPTIONS'])
def get_departments():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    departments = Department.query.all()
    return jsonify([
        {
            "dept_id": dept.dept_id,
            "dept_name": dept.dept_name,
            "status": dept.status,
        } for dept in departments
    ]), 200

# POST a new department
@departments_bp.route('/', methods=['POST'])
def create_department():
    try:
        data = request.json
        if not data.get('dept_name'):
            return jsonify({"error": "Department name is required"}), 400

        new_department = Department(
            dept_name=data['dept_name'],
            status=data.get('status', '1')  # Default to active status
        )

        db.session.add(new_department)
        db.session.commit()

        return jsonify({
            "message": "Department created successfully",
            "department": {
                "dept_id": new_department.dept_id,
                "dept_name": new_department.dept_name,
                "status": new_department.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# PUT to update an existing department
@departments_bp.route('/<int:dept_id>', methods=['PUT'])
def update_department(dept_id):
    try:
        data = request.json
        department = Department.query.get(dept_id)

        if not department:
            return jsonify({"error": "Department not found"}), 404

        if 'dept_name' in data:
            department.dept_name = data['dept_name']
        if 'status' in data:
            department.status = data['status']
        department.modified_on = datetime.utcnow()

        db.session.commit()
        return jsonify({
            "message": "Department updated successfully",
            "department": {
                "dept_id": department.dept_id,
                "dept_name": department.dept_name,
                "status": department.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE (hard delete) a department
@departments_bp.route('/<int:dept_id>', methods=['DELETE'])
def delete_department(dept_id):
    try:
        department = Department.query.get(dept_id)

        if not department:
            return jsonify({"error": "Department not found"}), 404

        db.session.delete(department)
        db.session.commit()

        return jsonify({
            "message": "Department deleted successfully",
            "dept_id": dept_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
