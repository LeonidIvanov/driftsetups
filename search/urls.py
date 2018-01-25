from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SearchListView.as_view(), name='search_list'),
]
