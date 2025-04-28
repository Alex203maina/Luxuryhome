import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
def generate_otp():
    """
    Generate a 6-digit OTP.
    """
    otp_chars = '0123456789'
    otp = ''.join(random.choice(otp_chars) for _ in range(6))
    return otp


def send_otp_email(email, otp,username):
    """
    Send a beautifully formatted OTP email to the provided email address.
    """
    subject = "Your LuxuryHomes Verification Code"
    
    # Context data for the template
    context = {
        'username': username,
        'otp': otp,
        'email': email,
        'support_email': 'support@luxuryhomes.com',
        'company_name': 'LuxuryHomes',
        'company_address': '123 Premium Avenue, Beverly Hills, CA 90210'
    }
    
    # Render HTML content
    html_content = render_to_string('emails/otp_email.html', context)
    
    # Create text version for email clients that don't support HTML
    text_content = strip_tags(f"""
    Your LuxuryHomes Verification Code
    
    Hello {username},
    
    Your verification code is: {otp}
    
    Please use this code to complete your registration. This code will expire in 10 minutes.
    
    If you didn't request this, please ignore this email or contact support.
    
    Thank you,
    LuxuryHomes Team
    """)
    
    # Create email message
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()