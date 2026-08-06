from extensions import db
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from utils.id_generator import generate_uuid
import enum

# User Table
# Default Inputs for the columns  
class UserRole(enum.Enum):
    ADMIN = "Admin"
    STAFF = "Staff"
    TREKKER = "Trekker"

# Basic User and Mandatory Details
class User(db.Model):
    __tablename__ = "users"

    # Internal Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Public ID
    user_uuid = db.Column(db.String(20), unique=True, nullable=False, default=lambda: generate_uuid("USR"))

    # Basic User Details
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.TREKKER)
    is_active = db.Column(db.Boolean, default=True)

    # Creation and Update Logs
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Last Login Details
    last_login = db.Column(db.DateTime, nullable=True)

    # Verification of details 
    email_verified = db.Column(db.Boolean, default=True)
    phone_verified = db.Column(db.Boolean, default=False)

    def set_password(self, plain_password):
        self.password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    # Relationships
    staff_profile = db.relationship("Staff", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trekker_profile = db.relationship("Trekker", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"

# Staff Table
# Default Inputs for the columns    
class Department(enum.Enum):
    OPERATIONS = "Operations"
    ADMINISTRATION = "Administration"
    SAFETY = "Safety"
    LOGISTICS = "Logistics"

class Designation(enum.Enum):
    GUIDE = "Guide"
    MANAGER = "Manager"
    COORDINATOR = "Coordinator"
    ACCOUNTANT = "Accountant"

class StaffStatus(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    DISMISSED = "Dismissed"
    
class Staff(db.Model):
    __tablename__ = "staff"

    staff_id = db.Column(db.Integer, primary_key=True)
    staff_uuid = db.Column(db.String(20), unique=True, nullable=False, default=lambda: generate_uuid("STF"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False,unique=True)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(Enum(Department))
    designation = db.Column(Enum(Designation))
    joining_date = db.Column(db.Date, nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    status = db.Column(Enum(StaffStatus), nullable=False, default=StaffStatus.ACTIVE)

    user = db.relationship( "User", back_populates="staff_profile")
    treks = db.relationship("Trek", back_populates="staff", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Staff {self.staff_uuid}>"

# Trekker Table
# Default Inputs for the columns  
class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class BloodGroup(enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class TrekkerStatus(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    BLOCKED = "Blocked"

class Trekker(db.Model):
    __tablename__ = "trekkers"

    trekker_id = db.Column(db.Integer, primary_key=True)
    trekker_uuid = db.Column(db.String(20), unique=True, nullable=False, default=lambda: generate_uuid("TRK"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(Enum(Gender), nullable=True)
    blood_group = db.Column(Enum(BloodGroup), nullable=True)
    emergency_contact = db.Column(db.String(10))
    medical_conditions = db.Column(db.Text)
    status = db.Column(Enum(TrekkerStatus), default=TrekkerStatus.ACTIVE)

    user = db.relationship("User", back_populates="trekker_profile")
    bookings = db.relationship("Booking", back_populates="trekker", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trekker {self.trekker_uuid}>"

# Trek Table
# Default Inputs for the columns  
class TrekDifficulty(enum.Enum):
    EASY = "Easy"
    MODERATE = "Moderate"
    DIFFICULT = "Difficult"
    EXTREME = "Extreme"

class TrekStatus(enum.Enum):
    UPCOMING = "Upcoming"
    OPEN = "Open"
    FULL = "Full"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Trek(db.Model):

    __tablename__ = "treks"

    trek_id = db.Column(db.Integer, primary_key=True)
    trek_uuid = db.Column(db.String(20), unique=True, nullable=False, default=lambda: generate_uuid("TREK"))
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"), nullable=False)
    trek_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150))
    duration_days = db.Column(db.Integer)
    difficulty = db.Column(Enum(TrekDifficulty), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(Enum(TrekStatus), nullable=False, default=TrekStatus.UPCOMING)
    available_slots = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    meeting_point = db.Column(db.String(255))

    staff = db.relationship("Staff", back_populates="treks")
    bookings = db.relationship("Booking", back_populates="trek", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trek {self.trek_name}>"
    
# Booking Details
# Default Inputs for the columns  

class BookingStatus(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class PaymentStatus(enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class Booking(db.Model):

    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer, primary_key=True)
    booking_uuid = db.Column(db.String(20), unique=True, nullable=False, default=lambda: generate_uuid("BOOK"))
    trekker_id = db.Column(db.Integer, db.ForeignKey("trekkers.trekker_id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.trek_id"))
    number_of_people = db.Column(db.Integer, nullable=False, default=1)
    booking_amount = db.Column(db.Numeric(10,2), nullable=False)
    booking_date = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    booking_status = db.Column(Enum(BookingStatus), nullable=False, default=BookingStatus.PENDING)
    payment_status = db.Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    payment_date = db.Column(db.DateTime)

    trekker = db.relationship("Trekker", back_populates="bookings")
    trek = db.relationship("Trek", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.booking_uuid}>"