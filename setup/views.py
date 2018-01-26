from itertools import chain
import re

from django.views.generic import TemplateView, CreateView, DetailView, View
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Setup, SetupImage, SetupVote
from .forms import SetupCreateForm, SetupImageCreateForm
from .forms import SetupEngineFieldCreateFormSet, SetupDrivetrainFieldCreateFormSet
from .forms import SetupSuspensionFieldCreateFormSet, SetupBrakesFieldCreateFormSet
from .forms import SetupWheelsFieldCreateFormSet, SetupExteriorFieldCreateFormSet
from .forms import SetupInteriorFieldCreateFormSet

from car.models import CarBrand, CarModel, CarSubModel


class SetupListView(TemplateView):
    template_name = 'setup_list.html'

    def get_context_data(self, **kwargs):
        context = super(SetupListView, self).get_context_data(**kwargs)
        if self.request.path == '/s/' or re.compile('/s/page/\d+/').match(self.request.path):
            setups = Setup.objects.all()
            context['base_url'] = redirect('setup_list').url
        else:
            if kwargs.get('sub_model_slug'):
                car_model = CarModel.objects.get(slug=kwargs.get('car_model_slug'))
                context['car'] = CarSubModel.objects.get(
                    slug=kwargs.get('sub_model_slug'),
                    car_model=car_model
                )
                context['base_url'] = redirect(
                    'sub_model_setup_list',
                    kwargs['car_model_slug'],
                    kwargs['sub_model_slug']
                ).url
            else:
                context['car'] = CarModel.objects.get(slug=kwargs.get('car_model_slug'))
                sub_models = CarSubModel.objects.filter(car_model=context['car'])
                sub_models_setups = []
                for sub_model in sub_models:
                    if sub_model.setups.all():
                        sub_models_setups.append(sub_model.setups.all())
                context['base_url'] = redirect(
                    'car_model_setup_list',
                    kwargs['car_model_slug']
                ).url
            context['car'].increase_views()
            setups = context['car'].setups.all()
            try:
                for sub_model_setups in sub_models_setups:
                    setups = list(
                        chain(
                            setups,
                            sub_model_setups
                        )
                    )
            except UnboundLocalError:
                pass
        paginator = Paginator(setups, 32)
        page = kwargs.get('page')
        if page:
            try:
                context['setups'] = paginator.page(page)
            except EmptyPage:
                raise Http404
        else:
            context['setups'] = paginator.page(1)
        return context

    def dispatch(self, request, *args, **kwargs):
        page = kwargs.get('page')
        if page == '1':
            if kwargs.get('sub_model_slug'):
                return redirect('sub_model_setup_list', kwargs['car_model_slug'], kwargs['sub_model_slug'], permanent=True)
            elif kwargs.get('car_model_slug'):
                return redirect('car_model_setup_list', kwargs['car_model_slug'], permanent=True)
            else:
                return redirect('setup_list', permanent=True)
        return super(SetupListView, self).dispatch(request, *args, **kwargs)


class SetupCreateView(LoginRequiredMixin, CreateView):
    model = Setup
    template_name = 'setup_create.html'
    form_class = SetupCreateForm

    def get_context_data(self, **kwargs):
        context = super(SetupCreateView, self).get_context_data(**kwargs)
        context['car_brands'] = CarBrand.objects.all()
        context['car_models'] = CarModel.objects.all()
        context['car_sub_models'] = CarSubModel.objects.all()
        if self.request.POST:
            context['images_form'] = SetupImageCreateForm(
                self.request.POST,
                self.request.FILES,
            )
            context['engine_fields_formset'] = SetupEngineFieldCreateFormSet(
                self.request.POST,
                prefix='engine_fields'
            )
            context['drivetrain_fields_formset'] = SetupDrivetrainFieldCreateFormSet(
                self.request.POST,
                prefix='drivetrain_fields'
            )
            context['suspension_fields_formset'] = SetupSuspensionFieldCreateFormSet(
                self.request.POST,
                prefix='suspension_fields'
            )
            context['brakes_fields_formset'] = SetupBrakesFieldCreateFormSet(
                self.request.POST,
                prefix='brakes_fields'
            )
            context['wheels_fields_formset'] = SetupWheelsFieldCreateFormSet(
                self.request.POST,
                prefix='wheels_fields'
            )
            context['exterior_fields_formset'] = SetupExteriorFieldCreateFormSet(
                self.request.POST,
                prefix='exterior_fields'
            )
            context['interior_fields_formset'] = SetupInteriorFieldCreateFormSet(
                self.request.POST,
                prefix='interior_fields'
            )
        else:
            context['images_form'] = SetupImageCreateForm()
            context['engine_fields_formset'] = SetupEngineFieldCreateFormSet(
                prefix='engine_fields'
            )
            context['drivetrain_fields_formset'] = SetupDrivetrainFieldCreateFormSet(
                prefix='drivetrain_fields'
            )
            context['suspension_fields_formset'] = SetupSuspensionFieldCreateFormSet(
                prefix='suspension_fields'
            )
            context['brakes_fields_formset'] = SetupBrakesFieldCreateFormSet(
                prefix='brakes_fields'
            )
            context['wheels_fields_formset'] = SetupWheelsFieldCreateFormSet(
                prefix='wheels_fields'
            )
            context['exterior_fields_formset'] = SetupExteriorFieldCreateFormSet(
                prefix='exterior_fields'
            )
            context['interior_fields_formset'] = SetupInteriorFieldCreateFormSet(
                prefix='interior_fields'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()

        if self.request.POST.get('car_sub_model'):
            car_sub_model_id = int(self.request.POST.get('car_sub_model'))
            form.instance.car = CarSubModel.objects.get(id=car_sub_model_id)
        else:
            car_model_id = int(self.request.POST.get('car_model'))
            form.instance.car = CarModel.objects.get(id=car_model_id)
        form.instance.creator = self.request.user
        self.object = form.save()

        images_form = context['images_form']
        engine_fields_formset = context['engine_fields_formset']
        drivetrain_fields_formset = context['drivetrain_fields_formset']
        suspension_fields_formset = context['suspension_fields_formset']
        brakes_fields_formset = context['brakes_fields_formset']
        wheels_fields_formset = context['wheels_fields_formset']
        exterior_fields_formset = context['exterior_fields_formset']
        interior_fields_formset = context['interior_fields_formset']
        if self.request.FILES:
            if images_form.is_valid():
                SetupImage.objects.create(
                    image=self.request.FILES.getlist('image')[0],
                    setup=self.object,
                    is_main=True
                )
                for file in self.request.FILES.getlist('image')[1:]:
                    SetupImage.objects.create(
                        image=file,
                        setup=self.object,
                        is_main=False
                    )

        with transaction.atomic():
            if engine_fields_formset.is_valid():
                engine_fields_formset.instance = self.object
                for form in engine_fields_formset:
                    form.instance.category = 0
                engine_fields_formset.save()
            if drivetrain_fields_formset.is_valid():
                drivetrain_fields_formset.instance = self.object
                for form in drivetrain_fields_formset:
                    form.instance.category = 1
                drivetrain_fields_formset.save()
            if suspension_fields_formset.is_valid():
                suspension_fields_formset.instance = self.object
                for form in suspension_fields_formset:
                    form.instance.category = 2
                suspension_fields_formset.save()
            if brakes_fields_formset.is_valid():
                brakes_fields_formset.instance = self.object
                for form in brakes_fields_formset:
                    form.instance.category = 3
                brakes_fields_formset.save()
            if wheels_fields_formset.is_valid():
                wheels_fields_formset.instance = self.object
                for form in wheels_fields_formset:
                    form.instance.category = 4
                wheels_fields_formset.save()
            if exterior_fields_formset.is_valid():
                exterior_fields_formset.instance = self.object
                for form in exterior_fields_formset:
                    form.instance.category = 5
                exterior_fields_formset.save()
            if interior_fields_formset.is_valid():
                interior_fields_formset.instance = self.object
                for form in interior_fields_formset:
                    form.instance.category = 6
                interior_fields_formset.save()

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SetupDetailView(TemplateView):
    template_name = 'setup_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SetupDetailView, self).get_context_data(**kwargs)
        context['setup'] = Setup.objects.get(slug=kwargs.get('setup_slug'))
        context['setup'].increase_views()
        return context


class SetupVoteUp(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        vote = SetupVote.objects.get(setup=kwargs.get('setup_slug'), user=request.user)
        vote = 1
        vote.save()
        return super(SetupVoteUp, self).get(request, *args, **kwargs)


class SetupVoteDown(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        vote = SetupVote.objects.get(setup=kwargs.get('setup_slug'), user=request.user)
        vote = 0
        vote.save()
        return super(SetupVoteDown, self).get(request, *args, **kwargs)
