# Step 1: Modify the DailyTask model
from app import db
from app.models.user import User
from app.models.project import Project

class DailyTask(db.Model):
    __tablename__ = 'daily_task'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='SET NULL'), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    
    daily_task = db.Column(db.Text, nullable=False)
    daily_work_hours = db.Column(db.Integer, default=8)
    priority = db.Column(db.String(20), default='medium')

    # Relationships
    user = db.relationship('User', backref=db.backref('daily_tasks', lazy=True, passive_deletes=True))
    project = db.relationship('Project', backref=db.backref('daily_tasks', lazy=True))

    @property
    def user_name(self):
        return self.user.user_name if self.user else None

    @property
    def project_description(self):
        return self.project.objective if self.project else None

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'project_id': self.project_id,
            'project_description': self.project_description,
            'daily_task': self.daily_task,
            'daily_work_hours': self.daily_work_hours,
            'priority': self.priority
        }

# Step 2: Update your database schema
# Run these commands after modifying the model
# flask db migrate -m "Set user_id nullable with ON DELETE SET NULL"
# flask db upgrade

# Step 3: No change needed in daily_task_bp or delete_user route
# The DB will handle nullifying user_id on user deletion
