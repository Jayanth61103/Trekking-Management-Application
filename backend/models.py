from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
import enum

db = SQLAlchemy()


class UserRole(enum.Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    TREKKER = "Trekker"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)

    # Update the column only with 3 values (Admin, Staff, Trekker)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.TREKKER)

    # Creates a Timestamp at the moment the user is created.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )

    # creates a time stamp everytime the object is updated.
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )
    # Names the Object (Entire Column of a user) under Username.
    def __repr__(self):
        return f"<User {self.username}>"
    