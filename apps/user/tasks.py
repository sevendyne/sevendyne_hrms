from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives


logger = get_task_logger(__name__)

@shared_task(name='send_hrms_credentials_email')
def send_hrms_signup_email_notification(subject, plain_message, from_email, to_email, html_message):
    try:
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

