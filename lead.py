from datetime import datetime
from app import db

class Lead(db.Model):
    __tablename__ = 'leads'

    lead_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lead_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    lead_description = db.Column(db.String(255), nullable=True)
    phone_no = db.Column(db.String(15), nullable=True)
    whatsapp_no = db.Column(db.String(15), nullable=True)
    email_id = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    lead_owner = db.Column(db.String(50), nullable=False)
    lead_status = db.Column(db.Enum(
        "new", "open", "initial_contact", "second_contact", 
        "no_response", "unqualified", "close"
    ), nullable=False, default="new")
    status_note = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_by = db.Column(db.String(50), nullable=True)
    modified_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "lead_id": self.lead_id,
            "lead_name": self.lead_name,
            "company_name": self.company_name,
            "lead_description": self.lead_description,
            "phone_no": self.phone_no,
            "whatsapp_no": self.whatsapp_no,
            "email_id": self.email_id,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "lead_owner": self.lead_owner,
            "lead_status": self.lead_status,
            "status_note": self.status_note,
            "created_by": self.created_by,
            "created_on": self.created_on,
            "modified_by": self.modified_by,
            "modified_on": self.modified_on
        }
