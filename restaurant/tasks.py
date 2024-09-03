from datetime import datetime

import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from restaurant.models import Reservation


@shared_task
def send_email(subject: str, message: str, to: list[str]):
    """Отправка писем функцией send_mail."""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to,
        )
        return "Successfully sent"
    except Exception as e:
        return f"Ошибка при отправке письма: {e}"


@shared_task
def check_reservation_statuses():
    """Проверяет статусы бронирований и меняет их по необходимости."""
    reservations = Reservation.objects.all().order_by("created_at")
    now = datetime.now(tz=pytz.UTC)
    for reservation in reservations:
        if (
            reservation.status == "created"
            and (now - reservation.created_at).total_seconds() > 3600 * 12
        ):
            reservation.status = "canceled"
            reservation.save()
        elif (
            reservation.status == "confirmed"
            and (reservation.date.today() - reservation.date).days > 0
        ):
            reservation.status = "completed"
            reservation.save()
