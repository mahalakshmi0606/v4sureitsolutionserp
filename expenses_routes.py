import os
from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from app import db
from app.models.expenses import Expense
from app.models.user import User
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError

expenses_bp = Blueprint('expenses_routes', __name__)

# Allowed file extensions
def allowed_file(filename):
    allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'pdf'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# GET all expenses
@expenses_bp.route('/expenses', methods=['GET'])
@cross_origin()
def get_all_expenses():
    try:
        expenses = Expense.query.all()
        final = []
        for expense_data in expenses:
            data = {
                "exp_id": expense_data.exp_id,
                "emp_id": expense_data.emp_id,
                "employee_name": expense_data.user.user_name if expense_data.user else None,
                "exp_description": expense_data.exp_description,
                "exp_attach": expense_data.exp_attach,
                "exp_amt": expense_data.exp_amt,
                "created_by": expense_data.created_by,
                "created_on": expense_data.created_on.isoformat() if expense_data.created_on else None,
                "created_by_action": expense_data.created_by_action,
                "action_by": expense_data.action_by,
            }
            final.append(data)
        return jsonify(final), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch expenses: {str(e)}"}), 400

# POST - Add new expense with file upload
@expenses_bp.route('/expenses', methods=['POST'])
@cross_origin()
def add_expense():
    try:
        form_data = request.form
        file = request.files.get('exp_attach')

        print("Form Data:", form_data)
        print("File:", file)

        required_fields = ['emp_id', 'exp_description', 'exp_amt', 'created_by']
        for field in required_fields:
            if not form_data.get(field):
                print(f"Missing: {field}")
                return jsonify({"error": f"{field.replace('_', ' ').title()} is required"}), 400

        # Validate user
        user = User.query.get(form_data['emp_id'])
        if not user:
            return jsonify({"error": "Employee not found"}), 404

        # Validate and convert amount
        try:
            amount = float(form_data['exp_amt'])
        except ValueError:
            return jsonify({"error": "Amount must be a valid number"}), 400

        # Handle file upload
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
        elif file:
            return jsonify({"error": "Invalid file type"}), 400

        # Create expense record
        expense = Expense(
            emp_id=form_data['emp_id'],
            exp_description=form_data['exp_description'],
            exp_attach=filename,
            exp_amt=amount,
            created_by=form_data['created_by'],
            created_on=datetime.utcnow(),
            created_by_action=form_data.get('created_by_action', 'Pending'),
            action_by=form_data.get('action_by', '')
        )
        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense created successfully",
            "exp_id": expense.exp_id,
            "employee_name": user.user_name
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create expense: {str(e)}"}), 500

# PUT - Update expense
@expenses_bp.route('/expenses/<int:exp_id>', methods=['PUT'])
@cross_origin()
def update_expense(exp_id):
    try:
        form_data = request.form
        file = request.files.get('exp_attach')
        expense = Expense.query.get(exp_id)

        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        if 'emp_id' in form_data:
            user = User.query.get(form_data['emp_id'])
            if not user:
                return jsonify({"error": "Employee not found"}), 404
            expense.emp_id = form_data['emp_id']

        if 'exp_description' in form_data:
            expense.exp_description = form_data['exp_description']

        if 'exp_amt' in form_data:
            try:
                expense.exp_amt = float(form_data['exp_amt'])
            except ValueError:
                return jsonify({"error": "Amount must be a valid number"}), 400

        if 'created_by' in form_data:
            expense.created_by = form_data['created_by']

        if 'created_by_action' in form_data:
            expense.created_by_action = form_data['created_by_action']

        if 'action_by' in form_data:
            expense.action_by = form_data['action_by']

        # Handle file upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            expense.exp_attach = filename
        elif file:
            return jsonify({"error": "Invalid file type"}), 400

        db.session.commit()

        return jsonify({
            "message": "Expense updated successfully",
            "exp_id": expense.exp_id,
            "employee_name": expense.user.user_name if expense.user else None
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update expense: {str(e)}"}), 400

# DELETE - Delete expense
@expenses_bp.route('/expenses/<int:exp_id>', methods=['DELETE'])
@cross_origin()
def delete_expense(exp_id):
    try:
        expense = Expense.query.get(exp_id)

        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        db.session.delete(expense)
        db.session.commit()

        return jsonify({"message": "Expense deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete expense: {str(e)}"}), 500
# PUT - Update expense action status
@expenses_bp.route('/expenses/<int:exp_id>/action', methods=['PUT'])
@cross_origin()
def update_expense_action(exp_id):
    try:
        data = request.get_json()
        action = data.get("action")
        action_by = data.get("action_by", "")

        if action not in ["Pending", "approved", "rejected"]:
            return jsonify({"error": "Invalid action status"}), 400

        expense = Expense.query.get(exp_id)
        if not expense:
            return jsonify({"error": "Expense not found"}), 404

        expense.created_by_action = action
        expense.action_by = action_by
        db.session.commit()

        return jsonify({"message": "Action status updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update action: {str(e)}"}), 400
