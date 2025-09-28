from datetime import datetime
from app import db

class LeadHistory(db.Model):
    __tablename__ = 'lead_history'

    lead_id = db.Column(db.Integer, db.ForeignKey('leads.lead_id'), primary_key=True, nullable=False)
    status_id = db.Column(db.Integer, primary_key=True, nullable=False)
    status_note = db.Column(db.String(255), nullable=True)
    created_by = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    modified_by = db.Column(db.String(50), nullable=True)
    modified_on = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)

    def to_dict(self):
        return {
            "lead_id": self.lead_id,
            "status_id": self.status_id,
            "status_note": self.status_note,
            "created_by": self.created_by,
            "created_on": self.created_on.isoformat() if self.created_on else None,
            "modified_by": self.modified_by,
            "modified_on": self.modified_on.isoformat() if self.modified_on else None
        }
