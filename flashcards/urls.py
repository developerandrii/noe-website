from django.urls import path
from . import views

urlpatterns = [
    path("",  views.DeckListView.as_view(), name="deck-list"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("decks/create/", views.CreateDeckView.as_view(), name="deck-create"),
    path("decks/<int:pk>/", views.DeckDetailView.as_view(), name="deck-detail"),
    path("decks/<int:deck_pk>/cards/create/", views.CreateCardView.as_view(), name="card-create"),
]