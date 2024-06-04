from django.urls import path

from . import views

app_name = 'webiel'

urlpatterns = [
    path('', views.home, name="home"),  # Home 
]