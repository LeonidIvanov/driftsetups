from django.views.generic import CreateView, DetailView
from django.urls import reverse
from django.contrib.auth import authenticate, login

from .models import User
from .forms import SignUpForm
from setup.models import Setup


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


class UserDetailView(DetailView):
    template_name = 'user_detail.html'
    model = User
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['setups'] = Setup.objects.filter(creator=context['profile'])
        return context
