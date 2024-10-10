import random
import string
from flask import current_app
from flask_mail import Message
from extensions import mail


def generate_otp():
    # Generate a random 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

def send_otp_email(email, otp):
    msg = Message("Your OTP Code", recipients=[email])
    msg.body = f"Your OTP code is: {otp}"
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
