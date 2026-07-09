from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from models import db, User, UserRole
from apis.auth import auth_bp

app = Flask(__name__)

# Enable CORS
CORS(app)

# JWT
app.config["JWT_SECRET_KEY"] = "your_super_secret_key"
jwt = JWTManager(app)

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Register APIs
app.register_blueprint(auth_bp)

def create_default_admin():

    # Check whether an admin already exists
    admin = User.query.filter_by(role=UserRole.ADMIN).first()

    if admin is None:
        default_admin = User(
            full_name="Admin",
            username="admin",
            email="admin@trek.com",
            password="Admin@123",
            phone="9999999999",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.session.add(default_admin)
        db.session.commit()
        print("Default Admin Created Successfully.")
    else:
        print("Default Admin Already Exists.")

with app.app_context():
    db.create_all()
    create_default_admin()

if __name__ == "__main__":
    app.run(debug=True)