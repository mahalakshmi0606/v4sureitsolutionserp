from flask import Blueprint, request, jsonify
from app.models.expense_approval import ExpenseApproval
from app import db
from datetime import datetime

expense_approval_bp = Blueprint('expense_approvals', __name__)

@expense_approval_bp.route('/expense_approvals', methods=['GET'])
def get_all_expense_approvals():
    expense_approvals = ExpenseApproval.query.all()
    return jsonify([approval.to_dict() for approval in expense_approvals]), 200

@expense_approval_bp.route('/expense_approvals/<int:exp_apr_id>', methods=['GET'])
def get_expense_approval_by_id(exp_apr_id):
    approval = ExpenseApproval.query.get_or_404(exp_apr_id)
    return jsonify(approval.to_dict()), 200

@expense_approval_bp.route('/expense_approvals', methods=['POST'])
def add_expense_approval():
    data = request.json
    expense_approval = ExpenseApproval(
        exp_id=data['exp_id'],
        emp_id=data['emp_id'],
        status_enum=data['status_enum'],
        apr_description=data.get('apr_description'),
        created_by=data['created_by']
    )
    db.session.add(expense_approval)
    db.session.commit()
    return jsonify({"message": " created successfully"}), 201

@expense_approval_bp.route('/expense_approvals/<int:exp_apr_id>', methods=['PUT'])
def update_expense_approval(exp_apr_id):
    data = request.json
    approval = ExpenseApproval.query.get_or_404(exp_apr_id)

    approval.status_enum = data.get('status_enum', approval.status_enum)
    approval.apr_description = data.get('apr_description', approval.apr_description)
    approval.modified_by = data.get('modified_by', approval.modified_by)

    db.session.commit()
    return jsonify({"message": "update successfully"}), 200

@expense_approval_bp.route('/expense_approvals/<int:exp_apr_id>', methods=['DELETE'])
def delete_expense_approval(exp_apr_id):
    approval = ExpenseApproval.query.get_or_404(exp_apr_id)
    db.session.delete(approval)
    db.session.commit()
    return jsonify({"message": "Expense approval record deleted successfully"}), 200
