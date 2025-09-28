import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # Make sure this is installed: pip install flask-jwt-extended
from flask_cors import CORS
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()  # Initialize the JWTManager instance


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS setup
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/login": {"origins": "*"},
        r"/register": {"origins": "*"}
    })

    # Import models inside app context
    with app.app_context():
        from app.models import enquiry, user_type, module, permission  # ✅ import your models

    # Register Blueprints
    from app.routes import (
        users_bp, departments_bp, lead_bp, customer_bp,
        expenses_bp, leads_history_bp, expense_approval_bp,
        login_bp, user_type_bp, useroffice_bp, enquiry_bp,
        project_bp, daily_task_bp, permission_leave_bp,
        attendance_bp, admin_attendance_bp
    )
    from app.routes.settings_routes import settings_bp  # ✅ new blueprint

    app.register_blueprint(departments_bp, url_prefix='/api/departments')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(lead_bp, url_prefix='/api')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(expenses_bp, url_prefix='/api')
    app.register_blueprint(leads_history_bp, url_prefix='/api/leads_history')
    app.register_blueprint(expense_approval_bp, url_prefix='/api')
    app.register_blueprint(user_type_bp, url_prefix='/api')
    app.register_blueprint(login_bp, url_prefix='/')
    app.register_blueprint(useroffice_bp, url_prefix='/api/office-hours')
    app.register_blueprint(enquiry_bp, url_prefix='/api/enquiry')
    app.register_blueprint(project_bp, url_prefix='/api/project')
    app.register_blueprint(daily_task_bp, url_prefix='/api/daily_task')
    app.register_blueprint(permission_leave_bp, url_prefix='/api/permission_leave')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(admin_attendance_bp, url_prefix='/api/admin')
    app.register_blueprint(settings_bp, url_prefix='/api')  # ✅ settings route

    # ✅ Route to serve uploaded files
    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        return send_from_directory(upload_folder, filename)

    # ✅ Health check route
    @app.route('/')
    def health_check():
        return jsonify({'status': 'healthy'})

    return app
