import secrets

from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from config.settings import ADMIN_EMAIL
from restaurant.models import Dish, Reservation
from restaurant.tasks import send_email
from restaurant.forms import ReservationForm


class Homepage(TemplateView):
    template_name = "restaurant/index.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        categories = [
            ("appetisers", "Закуски"),
            ("breakfasts", "Завтраки"),
            ("salads", "Салаты"),
            ("cold side dish", "Холодные блюда"),
            ("hot side dish", "Горячие блюда"),
            ("desserts", "Десерты"),
            ("drinks", "Напитки"),
            ("extra", "Дополнительно"),
        ]
        all_dishes = []
        for category in categories:
            dishes = Dish.objects.filter(category=category[0])
            if dishes:
                context_data[category] = dishes
                all_dishes.append({"name": category[1], "dishes": dishes})

        context_data["all"] = all_dishes
        return context_data

    def post(self, request, *args, **kwargs):
        name = str(request.POST.get('name'))
        phone = str(request.POST.get('phone'))
        email = str(request.POST.get('email'))
        subject = str(request.POST.get('subject'))
        message = str(request.POST.get('message'))
        # Если пользователь оставил email, то оправляем ему сообщение, что обращение получено
        if email:
            subject_for_user = 'Мы получили Ваше обращение'
            message_for_user = f'{name}, Ваше обращение доставлено администратору. Мы свяжемся с Вами в ближайшее время. Спасибо!'
            send_email.delay(subject_for_user, message_for_user, [email])
        # Отправляем письмо администратору
        subject_for_admin = 'Новое обращение на сайте'
        message_for_admin = f'Имя: {name}, Телефон: {phone}, Email: {email}, Тема: {subject}, Сообщение: {message}'
        send_email.delay(subject_for_admin, message_for_admin, [ADMIN_EMAIL])

        return redirect('restaurant:home')


class AboutPage(TemplateView):
    template_name = "restaurant/about.html"


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("restaurant:home")

    def form_valid(self, form):
        reservation = form.save()
        user = self.request.user
        reservation.user = user
        reservation.save()
        reservation_token = secrets.token_hex(16)
        reservation.reservation_token = reservation_token
        host = self.request.get_host()
        url = f"http://{host}/reservation_confirm/{reservation_token}/"
        to_email = user.email
        subject_for_user = "Подтвердите бронирование"
        message_for_user = f"Ваше бронирование на {reservation.date} создано. Для подтверждения перейдите по ссылке: {url}. В случае неподтвержденной брони, она автоматически отменяется через 24 часа"
        send_email.delay(subject_for_user, message_for_user, [to_email])
        return super().form_valid(form)


def reservation_confirm(request, reservation_token):
    reservation = get_object_or_404(Reservation, reservation_token=reservation_token)
    reservation.status = "confirmed"
    reservation.save()
    return redirect(reverse('restaurant:home'))


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation

    def get_queryset(self):
        reservations = Reservation.objects.filter(user=self.request.user)
        return reservations


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("restaurant:reservation_list")


def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = "canceled"
    reservation.save()
    return redirect(reverse('restaurant:reservation_list'))
