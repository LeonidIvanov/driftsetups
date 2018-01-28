from rest_framework import serializers

from car.models import CarBrand, CarModel, CarSubModel


class CarModelsByBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ('id', 'name')


class CarSubModelsByModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarSubModel
        fields = ('id', 'name')
