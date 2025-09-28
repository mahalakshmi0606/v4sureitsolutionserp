from app import db
from datetime import datetime
from sqlalchemy import func

class UserOffice(db.Model):
    __tablename__ = 'user_office_hours'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    date_in_office = db.Column(db.DateTime, nullable=False)
    leaving_office = db.Column(db.DateTime, nullable=False)
    total_hours = db.Column(db.Float)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to User model
    user = db.relationship('User', backref='office_hours')
    
    def __repr__(self):
        return f"<UserOffice {self.id} - User {self.user_id}>"
    
    def calculate_hours(self):
        if self.date_in_office and self.leaving_office:
            diff = self.leaving_office - self.date_in_office
            self.total_hours = round(diff.total_seconds() / 3600, 2)
        return self.total_hours
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.user_name if self.user else None,
            'date_in_office': self.date_in_office.isoformat() if self.date_in_office else None,
            'leaving_office': self.leaving_office.isoformat() if self.leaving_office else None,
            'total_hours': self.total_hours,
            'created_on': self.created_on.isoformat() if self.created_on else None
        }