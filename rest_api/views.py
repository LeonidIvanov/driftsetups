from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import authentication, permissions

from car.models import CarBrand, CarModel, CarSubModel

from .serializers import CarModelsByBrandSerializer, CarSubModelsByModelSerializer


class CarModelsByBrandList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CarModelsByBrandSerializer

    def get(self, request, format=None):
        brand_id = request.GET.get('brand_id')
        if brand_id:
            brand = CarBrand.objects.get(id=brand_id)
            car_models = CarModel.objects.filter(brand=brand)
            serializer = CarModelsByBrandSerializer(car_models, many=True)
            return Response(serializer.data)


class CarSubModelsByModelList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CarModelsByBrandSerializer

    def get(self, request, format=None):
        car_model_id = request.GET.get('car_model_id')
        if car_model_id:
            car_model = CarModel.objects.get(id=car_model_id)
            car_sub_models = CarSubModel.objects.filter(car_model=car_model)
            serializer = CarSubModelsByModelSerializer(car_sub_models, many=True)
            return Response(serializer.data)
