from django.core.mail import send_mail
from django.conf import settings

def send_email_to_user(subject, message, from_email, recipient_list):
    try:
        send_mail(
            subject,
            message,
            from_email = ["vedangrane430@gmail.com"],
            recipient_list = settings.EMAIL_HOST_USER,
            fail_silently=False,
        )
    except Exception as e:
        # Handle the exception (you might want to log this or show a message)
        print(f"Failed to send email: {str(e)}")
