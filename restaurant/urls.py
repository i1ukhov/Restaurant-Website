from django.urls import path

from restaurant.apps import RestaurantConfig

from restaurant.views import Homepage, AboutPage, ReservationCreateView, reservation_confirm, ReservationListView, \
    ReservationUpdateView, reservation_cancel

app_name = RestaurantConfig.name

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('reservation/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservation_confirm/<str:reservation_token>/', reservation_confirm, name='email_confirm'),
    path('my_reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/update/', ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservations/<int:pk>/cancel/', reservation_cancel, name='reservation_cancel'),
    ]
