from django.shortcuts import redirect
from django.views.generic import TemplateView

from config.settings import ADMIN_EMAIL
from restaurant.models import Dish
from restaurant.tasks import send_email


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
        # name, phone, email, subject, message
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
