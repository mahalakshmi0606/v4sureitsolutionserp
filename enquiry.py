from app import db
from datetime import datetime

class Enquiry(db.Model):
    __tablename__ = 'enquiry'

    enquiry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enquiry_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    whatsapp_number = db.Column(db.String(15))
    email_id = db.Column(db.String(100))
    address = db.Column(db.String(255))
    created_by = db.Column(db.String(100))  # Stores user_name
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    enquiry_status = db.Column(db.String(50), default='New')
    enquiry_notes = db.Column(db.Text)

    def __repr__(self):
        return f"<Enquiry {self.enquiry_id} - {self.enquiry_name}>"
