from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from extensions import db, jwt, mail

# Database Models
from models import db, User, UserRole

# API Blueprints
from apis.auth import auth_bp
from apis.admin import admin_bp
from apis.staff import staff_bp
from apis.trekker import trekker_bp

# Redis Client
from redis_client import redis_client

# Create Flask Application
app = Flask(__name__)

# CORS Configuration
CORS(
    app,
    origins=["http://localhost:5173"],
    supports_credentials=True
)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT Configuration

app.config["JWT_SECRET_KEY"] = "trekking_management_application_secret_key_2026"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


# MailHog Configuration
app.config["MAIL_SERVER"] = "localhost"
app.config["MAIL_PORT"] = 1025
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = None
app.config["MAIL_PASSWORD"] = None
app.config["MAIL_DEFAULT_SENDER"] = "admin@trekmate.com"

# Initialize Extensions
db.init_app(app)
jwt.init_app(app)
mail.init_app(app)

# JWT Blacklist Checker
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return redis_client.exists(jti)

# Register API Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(trekker_bp)

# Create Default Admin
def create_default_admin():

    admin = User.query.filter_by(role=UserRole.ADMIN).first()

    if admin:
        print("Default Admin Already Exists.")
        return

    default_admin = User(
        full_name="System Administrator",
        username="admin",
        email="admin@trek.com",
        password="Admin@123",     # Replace with hashed password later
        phone="9999999999",
        role=UserRole.ADMIN,
        is_active=True
    )
    db.session.add(default_admin)
    db.session.commit()
    print("Default Admin Created Successfully.")

# Initialize Database
with app.app_context():
    db.create_all()
    create_default_admin()

# Run Flask Application
if __name__ == "__main__":
    app.run(debug=True)