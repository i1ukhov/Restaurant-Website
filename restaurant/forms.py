from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import BooleanField, DateField
from django import forms

from restaurant.models import Reservation


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field, DateField):
                field.widget.attrs["class"] = "form-control datepicker"
            else:
                field.widget.attrs["class"] = "form-control"


class ReservationForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ("date", "table", "time", "user")
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', "input_formats": '%Y-%m-%d'}),
            'user': forms.HiddenInput
        }

    def clean_date(self):
        """Валидация введённой даты."""
        date = self.cleaned_data.get('date')
        today = date.today()
        till_date = today + timedelta(days=60)

        if date < today:
            raise ValidationError("Дата не может быть ранее текущей даты")
        elif date > till_date:
            raise ValidationError("Нельзя забронировать дальше, чем на 2 месяца вперёд")
        return date

    def clean_time(self):
        """Проверка, свободно ли время."""
        date = self.cleaned_data.get('date')
        table = self.cleaned_data.get('table')
        time = self.cleaned_data.get('time')
        user = self.data.get('user')
        if user:
            reserved = Reservation.objects.filter(~Q(user=user) & (Q(status="created") | Q(status="confirmed")),
                                                  date=date,
                                                  table=table)
        else:
            reserved = Reservation.objects.filter(Q(status="created") | Q(status="confirmed"),
                                                  date=date,
                                                  table=table)
        reserved_slots = []
        for obj in reserved:
            reserved_slots.extend(list(obj.time))
        slots_set = set(reserved_slots)
        reserved_slots_list = sorted(list(slots_set), key=lambda x: int(x))

        slots = [ts for ts in time]
        conflicting_slots = []
        for slot in slots:
            if slot in reserved_slots_list:
                conflicting_slots.append(slot)
        if len(conflicting_slots) > 0:
            raise ValidationError(f"Время на {', '.join(conflicting_slots)} уже занято. Выберите другой вариант")
        return time


class ReservationUpdateForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', "input_formats": '%Y-%m-%d'}),
        }
