from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives


logger = get_task_logger(__name__)

@shared_task(name='send_leave_email_notification')
def send_leave_email_notification(subject, plain_message, from_email, to_email, html_message):
    try:
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

@shared_task(name='send_employee_credentials_email_notification')
def send_employee_credentials_email_notification(subject, plain_message, from_email, to_email, html_message, cc_email):
    try:
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email], cc=[cc_email])
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

