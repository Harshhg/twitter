from django.conf import settings
from django.core.mail import send_mail


def send_email(subject, message, to_email=[], **kwargs):
    if not to_email:
        return

    send_mail(
        subject,
        message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=to_email,
        fail_silently=False,
    )

