from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^sitemap\.xml/$', views.SitemapXmlView.as_view(), name='sitemap'),
]
