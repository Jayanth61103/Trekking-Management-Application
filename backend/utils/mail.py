from flask_mail import Message
from extensions import mail

def send_staff_welcome_email(user_email,
                             full_name,
                             username,
                             password):
    subject = "Welcome to TrekMate"
    body = f"""
Hello {full_name},

Your Staff account has been created successfully.
Login Credentials
Username : {username}
Email : {user_email}
Temporary Password : {password}
Please login and change your password after your first login.
Regards,
TrekMate Administration
"""
    message = Message(
        subject=subject,
        recipients=[user_email],
        body=body
    )
    mail.send(message)