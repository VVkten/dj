from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Deck(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата редагування")
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        verbose_name="Рейтинг набору"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decks", verbose_name="Автор")

    def __str__(self):
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards", verbose_name="Набір карток")
    term = models.CharField(max_length=255, verbose_name="Термін")
    definition = models.CharField(max_length=255, verbose_name="Визначення")

    def __str__(self):
        return f"{self.term} - {self.definition}"
