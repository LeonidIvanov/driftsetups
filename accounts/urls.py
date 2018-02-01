from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^sign-up/$', views.SignUpView.as_view(), name='sign_up'),
    url(r'(?P<pk>[\d-]+)/$', views.UserDetailView.as_view(), name='user'),
]


