from django.urls import path

from restaurant.apps import RestaurantConfig

from restaurant.views import Homepage, AboutPage

app_name = RestaurantConfig.name

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    ]
