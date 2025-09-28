# app/models/user.py
from app import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)  # e.g., Super Admin, Admin
    email_id = db.Column(db.String(100), nullable=False, unique=True)
    phone_no = db.Column(db.String(15))
    status = db.Column(db.String(1), default="1")
    departments = db.Column(db.String(100))  # Store department name
    created_by = db.Column(db.String(100))
    created_on = db.Column(db.DateTime)
 
    def __repr__(self):
        return f"<User {self.user_name}>"
