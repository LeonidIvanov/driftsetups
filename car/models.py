from autoslug import AutoSlugField
from itertools import chain

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

from setup.models import Setup


class Engine(models.Model):
    name = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarImage(models.Model):
    image = models.ImageField(upload_to='cars/', blank=True, default=None, null=True)
    is_main = models.BooleanField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    car = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.image.url


class CarBrand(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', null=True, default=None, unique=True)

    class Meta:
        ordering = ['name']

    def get_setups(self):
        setups = chain()
        car_models = CarModel.objects.filter(brand=self)
        car_model_sub_models = chain()
        for car_model in car_models:
            setups = chain(
                setups,
                car_model.setups.all()
            )
            car_model_sub_models = chain(
                car_model_sub_models,
                car_model.get_sub_models(),
            )
        for car_sub_model in car_model_sub_models:
            setups = chain(
                setups,
                car_sub_model.setups.all(),
            )
        return setups

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(CarBrand)
    stock_engines = models.ManyToManyField(Engine, blank=True)
    setups = GenericRelation(Setup, related_query_name='car_model_setup')
    views = models.PositiveIntegerField(default=0)
    slug = AutoSlugField(populate_from='name', null=True, default=None, unique=True)
    images = GenericRelation(CarImage, related_query_name='car_model_images')

    class Meta:
        ordering = ['name']

    def increase_views(self):
        self.views += 1
        self.save()

    def get_main_image(self):
        return self.images.get(is_main=True)

    def get_sub_models(self):
        return CarSubModel.objects.filter(car_model=self)

    def get_setups(self):
        setups = chain()
        for car_sub_model in self.get_sub_models():
            setups = chain(
                setups,
                car_sub_model.setups.all(),
            )
        return setups

    def get_absolute_url(self):
        return reverse('car_model_detail', args=[str(self.brand.slug), str(self.slug)])

    def __str__(self):
        return '{0} {1}'.format(self.brand, self.name)
# CarModel.objects.filter(carsub_model__model__isnull=True) - models without sub_models


class CarSubModel(models.Model):
    name = models.CharField(max_length=100)
    car_model = models.ForeignKey(CarModel)
    stock_engines = models.ManyToManyField(Engine, blank=True)
    setups = GenericRelation(Setup, related_query_name='sub_model_setup')
    views = models.PositiveIntegerField(default=0)
    slug = AutoSlugField(populate_from='name', null=True, default=None, unique=True)
    images = GenericRelation(CarImage, related_query_name='sub_model_images')

    class Meta:
        ordering = ['name']

    def car_brand(self):
        return self.car_model.brand

    def increase_views(self):
        self.views += 1
        self.save()

    def get_main_image(self):
        return self.images.get(is_main=True)

    def get_absolute_url(self):
        return reverse('car_sub_model_detail', args=[str(self.car_model.brand.slug), str(self.car_model.slug), str(self.slug)])

    def __str__(self):
        return '{0} {1}'.format(self.car_model, self.name)
