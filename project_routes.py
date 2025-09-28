from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project
from app.models.enquiry import Enquiry
from datetime import datetime
from sqlalchemy.exc import IntegrityError

project_bp = Blueprint('project', __name__, url_prefix='/api/project')

@project_bp.route('/', methods=['GET'])
def get_all_projects():
    try:
        projects = Project.query.all()
        # Assuming Project has to_dict method, keep this as is
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in projects],
            'count': len(projects)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        proj = Project.query.get_or_404(project_id)
        return jsonify({
            'success': True,
            'data': proj.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if '404' in str(e) else 500

@project_bp.route('/', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        
        existing_project = Project.query.filter_by(enquiry_id=data['enquiry_id']).first()
        if existing_project:
            return jsonify({
                'success': False,
                'error': 'A project already exists for this enquiry'
            }), 400
        
        enquiry_obj = Enquiry.query.filter_by(
            enquiry_id=data['enquiry_id'],
            enquiry_status='Completed'
        ).first()
        
        if not enquiry_obj:
            return jsonify({
                'success': False,
                'error': 'Enquiry not found or not completed'
            }), 400
        
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if 'start_date' in data else None
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if 'end_date' in data else None
        
        proj = Project(
            enquiry_id=data['enquiry_id'],
            title=data['title'],
            category=data.get('category'),
            type=data.get('type'),
            objective=data.get('objective'),
            problem_statement=data.get('problem_statement'),
            proposed_solution=data.get('proposed_solution'),
            modules=data.get('modules'),
            frontend=data.get('frontend'),
            backend=data.get('backend'),
            database=data.get('database'),
            tools=data.get('tools'),
            other_tech=data.get('other_tech'),
            hardware=data.get('hardware'),
            software=data.get('software'),
            start_date=start_date,
            end_date=end_date,
            status=data.get('status', 'Not Started'),
            remarks=data.get('remarks')
        )
        
        db.session.add(proj)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': proj.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database integrity error'
        }), 400
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        proj = Project.query.get_or_404(project_id)
        data = request.get_json()
        
        for key in data:
            if key in ['start_date', 'end_date'] and data[key]:
                setattr(proj, key, datetime.strptime(data[key], '%Y-%m-%d').date())
            elif hasattr(proj, key):
                setattr(proj, key, data[key])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': proj.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        proj = Project.query.get_or_404(project_id)
        db.session.delete(proj)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Project deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@project_bp.route('/enquiry-options', methods=['GET'])
def get_enquiry_options():
    try:
        completed_enquiries = Enquiry.query.filter_by(enquiry_status='Completed').all()
        enquiries_without_projects = [
            e for e in completed_enquiries if not Project.query.filter_by(enquiry_id=e.enquiry_id).first()
        ]
        
        # Manual conversion to dict to avoid using e.to_dict()
        options = [{
            'enquiry_id': e.enquiry_id,
            'enquiry_name': e.enquiry_name,
            'company_name': e.company_name
        } for e in enquiries_without_projects]
        
        return jsonify({
            'success': True,
            'data': options
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
