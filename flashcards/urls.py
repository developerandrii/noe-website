from django.urls import path
from .views import RegisterView, DeckListView, CreateDeckView

urlpatterns = [
    path("", DeckListView.as_view(), name="deck-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("decks/create/", CreateDeckView.as_view(), name="deck-create")
]