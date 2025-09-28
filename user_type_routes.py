from flask import Blueprint, request, jsonify
from app import db
from app.models.user_type import UserType
from datetime import datetime

user_type_bp = Blueprint('user_type_bp', __name__)

# CREATE
@user_type_bp.route('/usertypes', methods=['POST'])
def create_user_type():
    data = request.get_json()
    user_type = data.get('type')

    if not user_type:
        return jsonify({'error': 'User type is required'}), 400

    new_user_type = UserType(type=user_type)
    db.session.add(new_user_type)
    db.session.commit()

    return jsonify({
        'id': new_user_type.id,
        'type': new_user_type.type,
        'createdOn': new_user_type.created_on.isoformat()
    }), 201

# READ ALL
@user_type_bp.route('/usertypes', methods=['GET'])
def get_user_types():
    user_types = UserType.query.order_by(UserType.id).all()
    result = [
        {
            'id': ut.id,
            'type': ut.type,
            'createdOn': ut.created_on.isoformat()
        }
        for ut in user_types
    ]
    return jsonify(result), 200

# UPDATE
@user_type_bp.route('/usertypes/<int:id>', methods=['PUT'])
def update_user_type(id):
    data = request.get_json()
    user_type = UserType.query.get_or_404(id)
    new_type = data.get('type')

    if not new_type:
        return jsonify({'error': 'User type is required'}), 400

    user_type.type = new_type
    db.session.commit()

    return jsonify({
        'id': user_type.id,
        'type': user_type.type,
        'createdOn': user_type.created_on.isoformat()
    }), 200

# DELETE
@user_type_bp.route('/usertypes/<int:id>', methods=['DELETE'])
def delete_user_type(id):
    user_type = UserType.query.get_or_404(id)
    db.session.delete(user_type)
    db.session.commit()

    return jsonify({'message': 'User type deleted successfully'}), 200
