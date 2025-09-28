from datetime import datetime
from app import db
from sqlalchemy import Enum

# Correct enum definition with proper values
status_enum = Enum('PENDING', 'APPROVED', 'REJECTED', name='status_enum')

class ExpenseApproval(db.Model):
    __tablename__ = 'expense_approval'

    exp_apr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exp_id = db.Column(db.Integer, db.ForeignKey('expenses.exp_id'), nullable=False)
    emp_id = db.Column(db.Integer, nullable=False)
    status_enum = db.Column(status_enum, nullable=False)
    apr_description = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified_by = db.Column(db.String(50), nullable=True)
    modified_on = db.Column(db.DateTime)

    expense = db.relationship('Expense', backref=db.backref('approvals', lazy=True))

    def to_dict(self):
        return {
            "exp_apr_id": self.exp_apr_id,
            "exp_id": self.exp_id,
            "emp_id": self.emp_id,
            "status_enum": self.status_enum,
            "apr_description": self.apr_description,
            "created_by": self.created_by,
            "created_on": self.created_on.isoformat(),
            "modified_by": self.modified_by,
            "modified_on": self.modified_on.isoformat() if self.modified_on else None
        }
