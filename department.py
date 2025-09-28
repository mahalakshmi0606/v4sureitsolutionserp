from app import db
from datetime import datetime, timezone

class Department(db.Model):

    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False, unique=True)

    status = db.Column(db.String(1), default="1")


    def __repr__(self):
        return f"<Department {self.dept_name}>"