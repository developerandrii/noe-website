from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from flashcards.models import Card


# ----- AUTHENTICATIONS VIEWS -----
class AccountLoginView(LoginView):
    template_name = "accounts/login.html"



class AccountLogoutView(LogoutView):
    pass



class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")



# ----- ACCOUNT VIEWS -----
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Show simple learning statistics for the logged-in user.
        context["deck_count"] = self.request.user.decks.count()
        context["card_count"] = Card.objects.filter(
            deck__owner=self.request.user,
        ).count()
        context["learned_card_count"] = Card.objects.filter(
            deck__owner=self.request.user,
            is_learned=True,
        ).count()

        return context