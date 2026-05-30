from django.urls import path
from .views import RegisterView, DeckListView

urlpatterns = [
    path("", DeckListView.as_view(), name="deck-list"),
    path("register/", RegisterView.as_view(), name="register"),
]