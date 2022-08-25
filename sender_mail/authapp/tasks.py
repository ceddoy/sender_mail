from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse

from sender_mail import settings


@shared_task
def send_verify_email(email, token):
    verify_link = reverse('verify', args=[token])
    subject = f'Подтверждение учетной записи {email}'
    message = f'Ссылка для активации учетной записи: {settings.BASE_URL}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=True)
