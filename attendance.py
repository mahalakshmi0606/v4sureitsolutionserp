from app import db
from datetime import datetime
import pytz  # Required for timezone support

# ✅ Function to return current time in IST (timezone-aware)
def current_time_ist():
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)

# ✅ Attendance Model Definition
class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=current_time_ist)  # ⏰ Save as IST time
    note = db.Column(db.String(200))
    user_type = db.Column(db.String(50), nullable=True)  # Optional field (Admin/Employee)
