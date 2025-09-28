# app/models/expense.py
from datetime import datetime
from app import db

class Expense(db.Model):
    __tablename__ = 'expenses'

    exp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    exp_description = db.Column(db.String(255), nullable=False)
    exp_attach = db.Column(db.String(255), nullable=True)
    exp_amt = db.Column(db.Float, nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by_action = db.Column(db.String(100), nullable=True)
    action_by = db.Column(db.String(100), nullable=True)

    # Define the relationship to User
    user = db.relationship('User', backref=db.backref('expenses', lazy=True))

    def __repr__(self):
        return f"<Expense {self.exp_description}>"