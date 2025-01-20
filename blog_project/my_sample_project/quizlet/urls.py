from django.urls import path, include
from . import views


app_name = "quizlet"

urlpatterns = [
    path('home_page/', views.home, name="home_page"),
    path('user/', views.user, name="account"),
    path('about/', views.about, name="about"),
    path('cards/', views.cards, name="cards"),
    path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),

]