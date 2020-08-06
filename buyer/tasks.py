from __future__ import absolute_import

from django.db import connection
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from celery import shared_task


def send_email(subject: str, template: str, email: str, link: str) -> None:

    if not connection.settings_dict['NAME'].rsplit('/')[-1].startswith('test_'):
        html_content = render_to_string(template, {'link': link})
        text_content = strip_tags(html_content)
        send_mail(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=html_content,
        )


@shared_task
def send_activation_email(email: str, token: str) -> None:
    send_email(
        'Activate Account for Paintly',
        'email/activate-account.html',
        email,
        f'http://localhost:3000/activate/{token}',
    )


@shared_task
def send_reset_email(email: str, token: str) -> None:
    send_email(
        'Reset Password for Paintly',
        'email/reset-password.html',
        email,
        f'http://localhost:3000/reset/{token}',
    )
