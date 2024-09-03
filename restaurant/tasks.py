from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(subject: str, message: str, to: list[str]):
    """Отправка писем функцией send_mail."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to
        )
        return "Successfully sent"
    except Exception as e:
        return f"Ошибка при отправке письма: {e}"


@shared_task
def check_reservation_statuses():
    """Проверяет статусы бронирований и меняет их по необходимости."""
    pass
