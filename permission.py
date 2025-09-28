from app import db
from datetime import datetime

class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_type = db.Column(db.String(100), nullable=False)  # Matches usertype.type
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id', ondelete='CASCADE'), nullable=False)

    has_access = db.Column(db.Boolean, default=False, nullable=False)
    show_action_column = db.Column(db.Boolean, default=False, nullable=False)

    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    module = db.relationship('Module', backref=db.backref('permissions', cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Permission user_type='{self.user_type}', module_id={self.module_id}, access={self.has_access}>"
