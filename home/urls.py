from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^privacy/$', views.PrivacyView.as_view(), name='privacy'),
    url(r'^tos/$', views.TOSView.as_view(), name='tos'),
]
