from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.models.officehours import UserOffice, db
from app.models.user import User

useroffice_bp = Blueprint('useroffice_routes', __name__)

# GET all office hours records
@useroffice_bp.route('/', methods=['GET'])
@cross_origin()
def get_all_office_hours():
    try:
        records = UserOffice.query.all()
        return jsonify([record.to_dict() for record in records]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch records: {str(e)}"}), 400

# GET office hours for specific user
@useroffice_bp.route('/user/<int:user_id>', methods=['GET'])
@cross_origin()
def get_user_office_hours(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        records = UserOffice.query.filter_by(user_id=user_id).all()
        return jsonify([record.to_dict() for record in records]), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch records: {str(e)}"}), 400

# POST - create new office hours record
@useroffice_bp.route('', methods=['POST'])
@cross_origin()
def add_office_hours():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'date_in_office', 'leaving_office']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field.replace('_', ' ').title()} is required"}), 400
        
        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Convert string dates to datetime objects
        try:
            date_in = datetime.fromisoformat(data['date_in_office'])
            date_out = datetime.fromisoformat(data['leaving_office'])
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
        
        # Validate date order
        if date_out <= date_in:
            return jsonify({"error": "Leaving time must be after entry time"}), 400
        
        # Create new record
        new_record = UserOffice(
            user_id=data['user_id'],
            date_in_office=date_in,
            leaving_office=date_out
        )
        new_record.calculate_hours()
        
        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({
            "message": "Record created successfully",
            "record": new_record.to_dict()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create record: {str(e)}"}), 500

# PUT - update office hours record
@useroffice_bp.route('/<int:record_id>', methods=['PUT'])
@cross_origin()
def update_office_hours(record_id):
    try:
        data = request.get_json()
        record = UserOffice.query.get(record_id)
        
        if not record:
            return jsonify({"error": "Record not found"}), 404
        
        # Update fields if provided
        if 'date_in_office' in data:
            try:
                record.date_in_office = datetime.fromisoformat(data['date_in_office'])
            except ValueError:
                return jsonify({"error": "Invalid date format for date_in_office"}), 400
        
        if 'leaving_office' in data:
            try:
                record.leaving_office = datetime.fromisoformat(data['leaving_office'])
            except ValueError:
                return jsonify({"error": "Invalid date format for leaving_office"}), 400
        
        # Validate date order if both are being updated
        if 'date_in_office' in data and 'leaving_office' in data:
            if record.leaving_office <= record.date_in_office:
                return jsonify({"error": "Leaving time must be after entry time"}), 400
        
        # Recalculate hours
        record.calculate_hours()
        db.session.commit()
        
        return jsonify({
            "message": "Record updated successfully",
            "record": record.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update record: {str(e)}"}), 400

# DELETE - delete office hours record
@useroffice_bp.route('/<int:record_id>', methods=['DELETE'])
@cross_origin()
def delete_office_hours(record_id):
    try:
        record = UserOffice.query.get(record_id)
        if not record:
            return jsonify({"error": "Record not found"}), 404
        
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete record: {str(e)}"}), 500

# GET statistics
@useroffice_bp.route('/stats', methods=['GET'])
@cross_origin()
def get_stats():
    try:
        # Total records
        total_records = db.session.query(func.count(UserOffice.id)).scalar()
        
        # Currently in office (where current time is between date_in and date_out)
        now = datetime.utcnow()
        current_in_office = UserOffice.query.filter(
            UserOffice.date_in_office <= now,
            UserOffice.leaving_office >= now
        ).count()
        
        return jsonify({
            "total_records": total_records,
            "currently_in_office": current_in_office
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get statistics: {str(e)}"}), 400