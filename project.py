from datetime import datetime
from app import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    project_id = db.Column(db.Integer, primary_key=True)
    enquiry_id = db.Column(db.Integer, db.ForeignKey('enquiry.enquiry_id'), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    type = db.Column(db.String(50))
    objective = db.Column(db.Text)
    problem_statement = db.Column(db.Text)
    proposed_solution = db.Column(db.Text)
    modules = db.Column(db.Text)
    frontend = db.Column(db.String(200))
    backend = db.Column(db.String(200))
    database = db.Column(db.String(200))
    tools = db.Column(db.String(200))
    other_tech = db.Column(db.String(200))
    hardware = db.Column(db.String(200))
    software = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Not Started')
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with Enquiry
    enquiry = db.relationship('Enquiry', backref='project', uselist=False)
    
    def to_dict(self):
        project_dict = {
            'project_id': self.project_id,
            'enquiry_id': self.enquiry_id,
            'title': self.title,
            'category': self.category,
            'type': self.type,
            'objective': self.objective,
            'problem_statement': self.problem_statement,
            'proposed_solution': self.proposed_solution,
            'modules': self.modules,
            'frontend': self.frontend,
            'backend': self.backend,
            'database': self.database,
            'tools': self.tools,
            'other_tech': self.other_tech,
            'hardware': self.hardware,
            'software': self.software,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'remarks': self.remarks,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        # Safely include enquiry details
        if self.enquiry:
            if hasattr(self.enquiry, 'to_dict'):
                project_dict['enquiry_details'] = self.enquiry.to_dict()
            else:
                project_dict['enquiry_details'] = {
                    'enquiry_id': self.enquiry.enquiry_id,
                    'enquiry_name': self.enquiry.enquiry_name,
                    'company_name': self.enquiry.company_name
                }
        else:
            project_dict['enquiry_details'] = None
            
        return project_dict