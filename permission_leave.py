from app import db
from datetime import datetime
from app.models.user import User

class PermissionLeave(db.Model):
    __tablename__ = 'permission_leave'

    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    leave_type = db.Column(db.String(20), nullable=False)  # 'permission' or 'leave'
    permission_type = db.Column(db.String(20))  # 'firstHalf' or 'secondHalf'
    leave_duration = db.Column(db.String(20))  # 'fullDay', 'firstHalf', etc.
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    reason = db.Column(db.String(50), nullable=False)
    mc_file = db.Column(db.String(200))
    explanation = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    action_by = db.Column(db.String(100))  # or appropriate size


    user = db.relationship('User', backref='permissions')

    def to_dict(self):
        return {
            "id": self.id,
            "permission_id": self.permission_id,
            "user_id": self.user_id,
            "user_name": self.user.user_name if self.user else None,
            "leave_type": self.leave_type,
            "permission_type": self.permission_type,
            "leave_duration": self.leave_duration,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "reason": self.reason,
            "mc_file": self.mc_file,
            "explanation": self.explanation,
            "status": self.status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "action_by": self.action_by
        }