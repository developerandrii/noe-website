from django.db import models
from django.contrib.auth.models import User


class Deck(models.Model):
    # User who owns the deck
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="decks",)
    # Deck name visible to the user
    name = models.CharField(max_length=100,)
    # Creation timestamp
    created_at = models.DateTimeField(auto_now_add=True,)


    def __str__(self):
        return self.name
    

class Card(models.Model):
    # Deck that owns the card
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="cards",)
    # Question 
    front = models.TextField()
    # Answer
    back = models.TextField()
    # Creation timestamp
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.front[:50]
