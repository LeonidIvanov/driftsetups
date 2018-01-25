from itertools import chain

from django import template

from car.models import CarSubModel, CarModel

register = template.Library()


@register.inclusion_tag('top_drift_cars.html')
def top_drift_cars():
    cars = sorted(list(
        chain(
            CarSubModel.objects.all(),
            CarModel.objects.all()
        )), key=lambda instance: instance.__str__())
    return {'top_drift_cars': cars}
