from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import Deck


class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = "flashcards/deck_list.html"
    context_object_name = "decks"

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)  



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

