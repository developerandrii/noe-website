from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.views import View

from .models import Deck, Card




# ----- DECK VIEWS -----
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



# ----- CARD VIEWS -----
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



# ---- STUDY VIEWS -----
class DeckStudyView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = "flashcards/deck_study.html"
    context_object_name = "deck"

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cards = self.object.cards.all()

        # The deck may have cards, even if all of them are already learned.
        context["has_cards"] = cards.exists()

        # Pick one random unlearned card from this deck.
        context["card"] = (
            cards
            .filter(is_learned=False)
            .order_by("?")
            .first()
        )

        return context



class CardStudyResultView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        card = get_object_or_404(
            Card,
            pk=self.kwargs["pk"],
            deck__owner=self.request.user,
        )

        study_result = request.POST.get("result")

        if study_result == "correct":
            card.correct_streak += 1

            if card.correct_streak >= card.target_streak:
                card.is_learned = True
                card.learned_at = timezone.now()

        elif study_result == "incorrect":
            card.correct_streak = 0
            card.is_learned = False
            card.learned_at = None

        card.save(
            update_fields=[
                "correct_streak",
                "is_learned",
                "learned_at",
            ]
        )

        return render(
            request,
            "flashcards/partials/card_study_progress.html",
            {"card": card},
        )





