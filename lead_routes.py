from flask import Blueprint, request, jsonify
from app.models.lead import db, Lead
from datetime import datetime

lead_bp = Blueprint('lead', __name__)

@lead_bp.route('/leads', methods=['GET'])
def get_leads():
    leads = Lead.query.all()
    return jsonify([lead.to_dict() for lead in leads]), 200

@lead_bp.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    return jsonify(lead.to_dict()), 200

@lead_bp.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    lead = Lead(
        lead_name=data['lead_name'],
        company_name=data['company_name'],
        lead_description=data.get('lead_description'),
        phone_no=data.get('phone_no'),
        whatsapp_no=data.get('whatsapp_no'),
        email_id=data.get('email_id'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        country=data.get('country'),
        lead_owner=data['lead_owner'],
        lead_status=data.get('lead_status', 'new'),
        status_note=data.get('status_note'),
        created_by=data['created_by']
    )
    db.session.add(lead)
    db.session.commit()
    return jsonify(lead.to_dict()), 201

@lead_bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    data = request.json
    lead = Lead.query.get_or_404(lead_id)

    lead.lead_name = data['lead_name']
    lead.company_name = data['company_name']
    lead.lead_description = data.get('lead_description')
    lead.phone_no = data.get('phone_no')
    lead.whatsapp_no = data.get('whatsapp_no')
    lead.email_id = data.get('email_id')
    lead.address = data.get('address')
    lead.city = data.get('city')
    lead.state = data.get('state')
    lead.country = data.get('country')
    lead.lead_owner = data['lead_owner']
    lead.lead_status = data.get('lead_status', lead.lead_status)
    lead.status_note = data.get('status_note')
    lead.modified_by = data.get('modified_by')

    db.session.commit()
    return jsonify(lead.to_dict()), 200

@lead_bp.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    return jsonify({"message": "Lead deleted successfully"}), 200
