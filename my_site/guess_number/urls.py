from django.urls import path
from . import views

urlpatterns = [
    path('', views.guess_number, name='guess_number'),
    path('guess_number', views.guess_number, name='guess_number'),

]