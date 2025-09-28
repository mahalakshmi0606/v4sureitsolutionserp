from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
from app import db
from app.models.enquiry import Enquiry
from app.models.user import User

enquiry_bp = Blueprint('enquiry_routes', __name__)

# POST - Create a new enquiry
@enquiry_bp.route('/enquiry', methods=['POST'])
@cross_origin()
def create_enquiry():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['enquiryName', 'createdBy']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400

        # Retrieve user by ID
        user = User.query.get(data['createdBy'])
        if not user:
            return jsonify({"error": "User not found for createdBy"}), 404

        # Create new enquiry instance
        new_enquiry = Enquiry(
            enquiry_name=data.get('enquiryName'),
            company_name=data.get('companyName', ''),
            phone_number=data.get('phoneNumber', ''),
            whatsapp_number=data.get('whatsappNumber', ''),
            email_id=data.get('emailId', ''),
            address=data.get('address', ''),
            created_by=user.user_name,
            enquiry_status=data.get('enquiryStatus', 'New'),
            enquiry_notes=data.get('enquiryNotes', '')
        )

        db.session.add(new_enquiry)
        db.session.commit()

        return jsonify({
            "message": "Enquiry created successfully",
            "enquiry": {
                "enquiry_id": new_enquiry.enquiry_id,
                "enquiry_name": new_enquiry.enquiry_name,
                "company_name": new_enquiry.company_name,
                "phone_number": new_enquiry.phone_number,
                "whatsapp_number": new_enquiry.whatsapp_number,
                "email_id": new_enquiry.email_id,
                "address": new_enquiry.address,
                "created_by": new_enquiry.created_by,
                "created_on": new_enquiry.created_on.isoformat(),
                "enquiry_status": new_enquiry.enquiry_status,
                "enquiry_notes": new_enquiry.enquiry_notes
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create enquiry: {str(e)}"}), 500

# GET - Retrieve all enquiries
@enquiry_bp.route('/enquiry', methods=['GET'])
@cross_origin()
def get_all_enquiries():
    try:
        enquiries = Enquiry.query.all()
        return jsonify([
            {
                "enquiry_id": e.enquiry_id,
                "enquiry_name": e.enquiry_name,
                "company_name": e.company_name,
                "phone_number": e.phone_number,
                "whatsapp_number": e.whatsapp_number,
                "email_id": e.email_id,
                "address": e.address,
                "created_by": e.created_by,
                "created_on": e.created_on.isoformat(),
                "enquiry_status": e.enquiry_status,
                "enquiry_notes": e.enquiry_notes
            }
            for e in enquiries
        ]), 200

    except Exception as e:
        return jsonify({"error": f"Failed to fetch enquiries: {str(e)}"}), 500

# PUT - Update an existing enquiry
@enquiry_bp.route('/enquiry/<int:enquiry_id>', methods=['PUT'])
@cross_origin()
def update_enquiry(enquiry_id):
    try:
        data = request.get_json()
        enquiry = Enquiry.query.get(enquiry_id)

        if not enquiry:
            return jsonify({"error": "Enquiry not found"}), 404

        enquiry.enquiry_name = data.get('enquiryName', enquiry.enquiry_name)
        enquiry.company_name = data.get('companyName', enquiry.company_name)
        enquiry.phone_number = data.get('phoneNumber', enquiry.phone_number)
        enquiry.whatsapp_number = data.get('whatsappNumber', enquiry.whatsapp_number)
        enquiry.email_id = data.get('emailId', enquiry.email_id)
        enquiry.address = data.get('address', enquiry.address)
        enquiry.enquiry_status = data.get('enquiryStatus', enquiry.enquiry_status)
        enquiry.enquiry_notes = data.get('enquiryNotes', enquiry.enquiry_notes)

        db.session.commit()

        return jsonify({"message": "Enquiry updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update enquiry: {str(e)}"}), 500

# DELETE - Remove an enquiry
@enquiry_bp.route('/enquiry/<int:enquiry_id>', methods=['DELETE'])
@cross_origin()
def delete_enquiry(enquiry_id):
    try:
        enquiry = Enquiry.query.get(enquiry_id)
        if not enquiry:
            return jsonify({"error": "Enquiry not found"}), 404

        db.session.delete(enquiry)
        db.session.commit()

        return jsonify({"message": "Enquiry deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete enquiry: {str(e)}"}), 500
