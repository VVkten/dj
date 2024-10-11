from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('calc/', include('calc.urls')),
    path('hello/', include('hello.urls')),
    path('guess_number/', include('guess_number.urls'))
]
