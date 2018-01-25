from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.CarBrandListView.as_view(),
        name='car_brand_list'),
    url(
        r'^(?P<slug>[\w\d-]+)/$',
        views.CarBrandDetailView.as_view(),
        name='car_brand_detail'),
    url(
        r'^(?P<brand_slug>[\w\d-]+)/(?P<slug>[\w\d-]+)/$',
        views.CarModelDetailView.as_view(),
        name='car_model_detail'),
    url(
        r'^(?P<brand_slug>[\w\d-]+)/(?P<model_slug>[\w\d-]+)/(?P<slug>[\w\d-]+)/$',
        views.CarSubModelDetailView.as_view(),
        name='car_sub_model_detail'),
]


