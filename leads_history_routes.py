from flask import Blueprint, request, jsonify
from app.models.leads_history import LeadHistory
from app import db
from datetime import datetime

leads_history_bp = Blueprint('leads_history', __name__)

@leads_history_bp.route('/leads_history', methods=['GET', 'POST'])
def leads_history():
    if request.method == 'GET':
        try:
            histories = LeadHistory.query.all()
            return jsonify([history.to_dict() for history in histories]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    elif request.method == 'POST':
        data = request.json
        try:
            # Validate required fields
            if not all(key in data for key in ['lead_id', 'status_id', 'created_by']):
                return jsonify({"error": "Missing required fields"}), 400
                
            history = LeadHistory(
                lead_id=data['lead_id'],
                status_id=data['status_id'],
                status_note=data.get('status_note', ''),
                created_by=data['created_by'],
                created_on=datetime.fromisoformat(data['created_on']) if 'created_on' in data else None
            )
            
            db.session.add(history)
            db.session.commit()
            
            return jsonify(history.to_dict()), 201
            
        except ValueError as e:
            return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

@leads_history_bp.route('/leads_history/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def lead_history_by_id(id):
    try:
        history = LeadHistory.query.get_or_404(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    
    if request.method == 'GET':
        return jsonify(history.to_dict()), 200
        
    elif request.method == 'PUT':
        data = request.json
        try:
            if 'lead_id' in data:
                history.lead_id = data['lead_id']
            if 'status_id' in data:
                history.status_id = data['status_id']
            if 'status_note' in data:
                history.status_note = data['status_note']
            if 'modified_by' in data:
                history.modified_by = data['modified_by']
                
            db.session.commit()
            return jsonify(history.to_dict()), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
            
    elif request.method == 'DELETE':
        try:
            db.session.delete(history)
            db.session.commit()
            return jsonify({"message": "Lead history deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500