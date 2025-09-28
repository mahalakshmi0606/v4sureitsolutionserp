from app import db
from datetime import datetime

class UserType(db.Model):
    __tablename__ = 'user_types'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserType {self.type}>"