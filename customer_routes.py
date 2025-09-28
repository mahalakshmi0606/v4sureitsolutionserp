from flask import Blueprint, request, jsonify, send_file
from app.models.customer import Customer
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import os
from werkzeug.utils import secure_filename
from app import Config

customer_bp = Blueprint('customer', __name__, url_prefix='/api/customers')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@customer_bp.route('', methods=['GET'])
def get_all_customers():
    try:
        customers = Customer.query.order_by(Customer.id).all()
        return jsonify([customer.to_dict() for customer in customers]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer_by_id(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify(customer.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@customer_bp.route('', methods=['POST'])
def add_customer():
    try:
        data = request.form.to_dict()
        file = request.files.get('attachment')
        
        # Required fields validation
        required_fields = ['customer_name', 'email_id', 'phone_no', 'address', 'city', 'country', 'created_by']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Handle file upload
        attachment_path = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(Config.UPLOAD_FOLDER):
                os.makedirs(Config.UPLOAD_FOLDER)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            attachment_path = filepath
        
        # Create new customer
        customer = Customer(
            customer_name=data['customer_name'],
            company_name=data.get('company_name'),
            email_id=data['email_id'],
            phone_no=data['phone_no'],
            whatsapp_no=data.get('whatsapp_no'),
            address=data['address'],
            city=data['city'],
            state=data.get('state'),
            country=data['country'],
            attachment=attachment_path,
            created_by=data['created_by']
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'message': 'Customer created successfully',
            'customer': customer.to_dict()
        }), 201
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.form.to_dict()
        file = request.files.get('attachment')
        customer = Customer.query.get_or_404(customer_id)

        # Handle file upload
        if file and allowed_file(file.filename):
            # Delete old file if exists
            if customer.attachment and os.path.exists(customer.attachment):
                os.remove(customer.attachment)
            
            # Save new file
            filename = secure_filename(file.filename)
            if not os.path.exists(Config.UPLOAD_FOLDER):
                os.makedirs(Config.UPLOAD_FOLDER)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
            data['attachment'] = filepath

        # Update fields if they exist in the request
        update_fields = [
            'customer_name', 'company_name', 'email_id', 
            'phone_no', 'whatsapp_no', 'address', 
            'city', 'state', 'country', 'attachment'
        ]
        
        for field in update_fields:
            if field in data:
                setattr(customer, field, data[field])
        
        # Always update modified info
        customer.modified_by = data.get('modified_by', customer.created_by)
        customer.modified_on = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Customer updated successfully',
            'customer': customer.to_dict()
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        
        # Delete associated file if exists
        if customer.attachment and os.path.exists(customer.attachment):
            os.remove(customer.attachment)
            
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@customer_bp.route('/download/<int:customer_id>', methods=['GET'])
def download_attachment(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        if not customer.attachment or not os.path.exists(customer.attachment):
            return jsonify({'error': 'File not found'}), 404
            
        return send_file(customer.attachment, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 400