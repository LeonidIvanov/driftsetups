from django.contrib import admin

from .models import CarBrand, CarModel, CarSubModel, Engine, CarImage


class CarBrandAdmin(admin.ModelAdmin):
    model = CarBrand
    ordering = ('name',)


class CarModelAdmin(admin.ModelAdmin):
    model = CarBrand
    fields = ('name', 'brand', 'stock_engines',)
    ordering = ('name',)
    list_display = ('name', 'brand',)
    filter_vertical = ('stock_engines',)
    search_fields = ('name',)


class CarSubModelAdmin(admin.ModelAdmin):
    model = CarBrand
    fields = ('name', 'car_model', 'stock_engines',)
    ordering = ('name',)
    list_display = ('name', 'car_model', 'get_car_brand',)
    filter_vertical = ('stock_engines',)
    search_fields = ('name',)


class EngineAdmin(admin.ModelAdmin):
    model = Engine
    fields = ('name', 'producer',)
    ordering = ('name',)
    list_display = ('name', 'producer',)
    search_fields = ('name',)


admin.site.register(CarBrand, CarBrandAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarSubModel, CarSubModelAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(CarImage)
