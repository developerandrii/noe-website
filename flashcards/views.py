from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Deck, Card


class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = "flashcards/deck_list.html"
    context_object_name = "decks"

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)  



class CreateDeckView(LoginRequiredMixin, CreateView):
    model = Deck
    fields = ['name']
    template_name = "flashcards/deck_form.html"
    success_url = reverse_lazy("deck-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    


class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = "flashcards/deck_detail.html"
    context_object_name = "deck"

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)



class CreateCardView(LoginRequiredMixin, CreateView):
    model = Card
    fields = ["front", "back"]
    template_name = "flashcards/card_form.html"

    def form_valid(self, form):
        deck = get_object_or_404(
            Deck,
            pk=self.kwargs["deck_pk"],
            owner=self.request.user,
        )

        form.instance.deck = deck
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "deck-detail",
            kwargs={"pk": self.object.deck.pk},
        )



class UpdateDeckView(LoginRequiredMixin, UpdateView):
    model = Deck
    fields = ["name"]
    template_name = "flashcards/deck_form.html"
    success_url = reverse_lazy("deck-list")

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)



class DeleteDeckView(LoginRequiredMixin, DeleteView):
    model = Deck
    template_name = "flashcards/deck_confirm_delete.html"
    success_url = reverse_lazy("deck-list")

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)
    


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "flashcards/card_detail.html"
    context_object_name = "card"

    def get_queryset(self):
        return Card.objects.filter(deck__owner=self.request.user)



class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    fields = ["front", "back"]
    template_name = "flashcards/card_form.html"

    def get_queryset(self):
        return Card.objects.filter(deck__owner=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy(
            "deck-detail",
            kwargs={"pk": self.object.deck.pk},
        )



class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "flashcards/card_confirm_delete.html"

    def get_queryset(self):
        return Card.objects.filter(deck__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy(
            "deck-detail",
            kwargs={"pk": self.object.deck.pk},
        )



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

