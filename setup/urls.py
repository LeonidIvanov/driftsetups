from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.SetupListView.as_view(), name='setup_list'),
    url(r'^page/(?P<page>\d)/$',
        views.SetupListView.as_view(),
        name='setup_list_pagination'
        ),
    url(r'^add/$',
        views.SetupCreateView.as_view(),
        name='setup_create'
        ),
    url(r'^c/(?P<car_model_slug>[\w\d-]+)/$',
        views.SetupListView.as_view(),
        name='car_model_setup_list'
        ),
    url(r'^c/(?P<car_model_slug>[\w\d-]+)/page/(?P<page>\d)/$',
        views.SetupListView.as_view(),
        name='car_model_setup_list_pagination'
        ),
    url(r'^c/(?P<car_model_slug>[\w\d-]+)/(?P<sub_model_slug>[\w\d-]+)/$',
        views.SetupListView.as_view(),
        name='sub_model_setup_list'
        ),
    url(r'^c/(?P<car_model_slug>[\w\d-]+)/(?P<sub_model_slug>[\w\d-]+)/page/(?P<page>\d)/$',
        views.SetupListView.as_view(),
        name='sub_model_setup_list_pagination'
        ),
    url(r'^(?P<setup_slug>[\w\d-]+)/$',
        views.SetupDetailView.as_view(),
        name='setup_detail'
        ),
    url(r'^(?P<setup_slug>[\w\d-]+)/vote_up/$',
        views.SetupVoteUp.as_view(),
        name='setup_vote_up'
        ),
    url(r'^(?P<setup_slug>[\w\d-]+)/vote_down/$',
        views.SetupVoteDown.as_view(),
        name='setup_vote_down'
        ),
]
