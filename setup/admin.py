from django.contrib import admin

from .models import Setup, SetupImage, SetupField


# class CarBrandAdmin(admin.ModelAdmin):
#     model = CarBrand
#     ordering = ('name',)
#
#
# class CarModelAdmin(admin.ModelAdmin):
#     model = CarBrand
#     fields = ('name', 'brand', 'stock_engines',)
#     ordering = ('name',)
#     list_display = ('name', 'brand',)
#     filter_vertical = ('stock_engines',)
#
#
# class CarSubModelAdmin(admin.ModelAdmin):
#     model = CarBrand
#     fields = ('name', 'model', 'stock_engines',)
#     ordering = ('name',)
#     list_display = ('name', 'model', 'car_brand',)
#     filter_vertical = ('stock_engines',)
#
#
# class EngineAdmin(admin.ModelAdmin):
#     model = Engine
#     fields = ('name', 'producer',)
#     ordering = ('name',)
#     list_display = ('name', 'producer',)
#     search_fields = ('name',)


admin.site.register(Setup)
admin.site.register(SetupField)
admin.site.register(SetupImage)
