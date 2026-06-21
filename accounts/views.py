from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


# ----- AUTHENTICATIONS VIEWS -----
class AccountLoginView(LoginView):
    template_name = "accounts/login.html"



class AccountLogoutView(LogoutView):
    pass




class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")