from flask import Blueprint, request, jsonify
from app import db
from app.models.module import Module
from app.models.permission import Permission
from app.models.user_type import UserType
from datetime import datetime

settings_bp = Blueprint('settings', __name__)

# -------------------- MODULES --------------------

@settings_bp.route('/modules', methods=['GET'])
def get_modules():
    modules = Module.query.all()
    return jsonify([{"id": m.id, "name": m.name} for m in modules]), 200


@settings_bp.route('/modules', methods=['POST'])
def add_module():
    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Module name is required"}), 400

    if Module.query.filter_by(name=name).first():
        return jsonify({"error": "Module already exists"}), 400

    new_module = Module(name=name)
    db.session.add(new_module)
    db.session.commit()
    return jsonify({"id": new_module.id, "name": new_module.name}), 201


@settings_bp.route('/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    data = request.get_json()
    name = data.get("name", "").strip()

    if not name:
        return jsonify({"error": "Module name is required"}), 400

    existing_module = Module.query.get(module_id)
    if not existing_module:
        return jsonify({"error": "Module not found"}), 404

    # Check for name duplication
    if Module.query.filter(Module.name == name, Module.id != module_id).first():
        return jsonify({"error": "Another module with this name already exists"}), 400

    existing_module.name = name
    db.session.commit()
    return jsonify({"id": existing_module.id, "name": existing_module.name}), 200


@settings_bp.route('/modules/<int:module_id>', methods=['DELETE'])
def delete_module(module_id):
    module = Module.query.get(module_id)
    if not module:
        return jsonify({"error": "Module not found"}), 404

    # Optionally delete related permissions
    Permission.query.filter_by(module_id=module_id).delete()

    db.session.delete(module)
    db.session.commit()
    return jsonify({"message": "Module deleted successfully"}), 200

# -------------------- PERMISSIONS --------------------

@settings_bp.route('/permissions', methods=['GET'])
def get_permissions():
    permissions = Permission.query.all()
    modules = Module.query.all()
    user_types = UserType.query.all()

    result = []

    for user_type in user_types:
        for module in modules:
            existing = next(
                (p for p in permissions if p.user_type == user_type.type and p.module_id == module.id),
                None
            )

            result.append({
                "user_type": user_type.type,
                "module_id": module.id,
                "module_name": module.name,
                "has_access": existing.has_access if existing else False,
            })

    return jsonify(result), 200


@settings_bp.route('/permissions', methods=['POST'])
def set_permissions():
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of permission objects"}), 400

    for item in data:
        user_type = item.get("user_type")
        module_id = item.get("module_id")
        has_access = item.get("has_access", False)

        if not user_type or not module_id:
            continue

        if not Module.query.get(module_id):
            continue
        if not UserType.query.filter_by(type=user_type).first():
            continue

        existing = Permission.query.filter_by(user_type=user_type, module_id=module_id).first()
        if existing:
            existing.has_access = has_access
            existing.show_action_column = False
        else:
            new_perm = Permission(
                user_type=user_type,
                module_id=module_id,
                has_access=has_access,
                show_action_column=False,
                created_on=datetime.utcnow()
            )
            db.session.add(new_perm)

    db.session.commit()
    return jsonify({"message": "Permissions updated successfully"}), 200


# -------------------- USER TYPES --------------------

@settings_bp.route('/api/usertypes', methods=['GET'])
def get_user_types():
    usertypes = UserType.query.all()
    return jsonify([{"id": u.id, "type": u.type} for u in usertypes]), 200
