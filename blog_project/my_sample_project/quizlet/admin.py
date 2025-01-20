from django.contrib import admin
from .models import Deck, Card

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'rating', 'created_at', 'updated_at')
    search_fields = ('name', 'author__username')
    list_filter = ('rating', 'created_at', 'author')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('term', 'definition', 'deck')
    search_fields = ('term', 'definition', 'deck__name')
