from django.shortcuts import render, get_object_or_404
from .models import Deck

# Create your views here.
def home(request):
    decks = Deck.objects.all()
    return render(request, "home.html", {'decks': decks})

def user(request):
    decks = Deck.objects.filter(author=request.user)
    return render(request, "account.html", {'decks': decks})

def about(request):
    return render(request, "about_us.html")

def cards(request):
    decks = Deck.objects.all()
    return render(request, "cards.html", {'decks': decks})


def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    return render(request, 'deck_detail.html', {'deck': deck})
