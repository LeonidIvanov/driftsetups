from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^car_models_by_brand/$', views.CarModelsByBrandList.as_view(), name='api_car_models_by_brand'),
    url(r'^car_sub_models_by_model/$', views.CarSubModelsByModelList.as_view(), name='api_car_sub_models_by_model'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
