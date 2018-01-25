from django.views.generic import CreateView
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .forms import SignUpForm


class SignUpView(CreateView):
    template_name = 'register.html'
    form_class = SignUpForm

    def get_success_url(self):
        return reverse('place_list')

    def form_valid(self, form):
        print('Valid!')
        valid = super(SignUpView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return valid