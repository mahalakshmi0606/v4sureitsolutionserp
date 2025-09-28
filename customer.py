from app import db
from datetime import datetime
import os

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100))
    email_id = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(20))
    whatsapp_no = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    attachment = db.Column(db.String(255))  # Stores the file path
    created_by = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    modified_by = db.Column(db.String(50))
    modified_on = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'company_name': self.company_name,
            'email_id': self.email_id,
            'phone_no': self.phone_no,
            'whatsapp_no': self.whatsapp_no,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'attachment': self.attachment,
            'created_by': self.created_by,
            'created_on': self.created_on.isoformat() if self.created_on else None,
            'modified_by': self.modified_by,
            'modified_on': self.modified_on.isoformat() if self.modified_on else None
        }

    def __repr__(self):
        return f'<Customer {self.customer_name}>'