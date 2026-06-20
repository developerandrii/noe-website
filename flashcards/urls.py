from django.urls import path
from . import views

urlpatterns = [
   # Decks
    path("",  views.DeckListView.as_view(), name="deck-list"),
    path("decks/create/", views.CreateDeckView.as_view(), name="deck-create"),
    path("decks/<int:pk>/", views.DeckDetailView.as_view(), name="deck-detail"),
    path("decks/<int:deck_pk>/cards/create/", views.CreateCardView.as_view(), name="card-create"),
    path('decks/<int:pk>/edit/', views.UpdateDeckView.as_view(), name='deck-update'),
    path("decks/<int:pk>/delete/", views.DeleteDeckView.as_view(), name="deck-delete"),
    # Cards
    path("cards/<int:pk>/", views.CardDetailView.as_view(), name="card-detail"),
    path("cards/<int:pk>/edit/", views.CardUpdateView.as_view(), name="card-update"),
    path("cards/<int:pk>/delete/", views.CardDeleteView.as_view(), name="card-delete"),
    # Study
    path("decks/<int:pk>/study/", views.DeckStudyView.as_view(), name="deck-study"),
    path("cards/<int:pk>/study-result/", views.CardStudyResultView.as_view(), name="card-study-result"),
]