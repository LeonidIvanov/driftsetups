from django.views.generic import ListView, DetailView

from .models import CarBrand, CarModel, CarSubModel


class CarBrandListView(ListView):
    model = CarBrand
    template_name = 'car_list.html'
    context_object_name = 'car_list'


class CarBrandDetailView(DetailView):
    model = CarBrand
    template_name = 'car_list.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super(CarBrandDetailView, self).get_context_data(**kwargs)
        context['car_list'] = CarModel.objects.filter(brand=context['car'])
        context['setups'] = context['car'].get_setups()
        return context


class CarModelDetailView(DetailView):
    model = CarModel
    template_name = 'car_list.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super(CarModelDetailView, self).get_context_data(**kwargs)
        context['car_list'] = CarSubModel.objects.filter(car_model=context['car'])
        context['setups'] = context['car'].get_setups()
        return context


class CarSubModelDetailView(DetailView):
    model = CarSubModel
    template_name = 'car_list.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super(CarSubModelDetailView, self).get_context_data(**kwargs)
        context['setups'] = context['car'].setups.all()
        return context