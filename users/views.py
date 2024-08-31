import secrets

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.set_password(user.password)
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения почты перейдите по ссылке: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ResetPassword(TemplateView):
    def get(self, request):
        return render(request, 'users/reset_password.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        new_password = secrets.token_hex(16)
        user.set_password(new_password)
        user.save()
        message = f'Новый сгенерированный пароль: {new_password}'
        send_mail(
            subject='Изменение пароля',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
