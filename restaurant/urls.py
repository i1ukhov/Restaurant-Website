from django.urls import path

from restaurant.apps import RestaurantConfig

from restaurant.views import Homepage
app_name = RestaurantConfig.name

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    ]
