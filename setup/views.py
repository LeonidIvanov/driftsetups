from itertools import chain
import re

from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import Setup, SetupVote, SetupField
from .forms import SetupCreateForm, SetupImageCreateFormSet
from .forms import SetupEngineFieldCreateFormSet, SetupDrivetrainFieldCreateFormSet
from .forms import SetupSuspensionFieldCreateFormSet, SetupBrakesFieldCreateFormSet
from .forms import SetupWheelsFieldCreateFormSet, SetupExteriorFieldCreateFormSet
from .forms import SetupInteriorFieldCreateFormSet

from car.models import CarBrand, CarModel, CarSubModel


class SetupListView(TemplateView):
    template_name = 'setup_list.html'

    def get_context_data(self, **kwargs):
        context = super(SetupListView, self).get_context_data(**kwargs)
        if self.request.path in ['/s/', '/ru/s/'] or re.compile('/s/page/\d+/').match(self.request.path) or re.compile('/ru/s/page/\d+/').match(self.request.path):
            setups_by_votes = sorted(
                Setup.objects.all(),
                key=lambda s: s.get_votes_total(),
                reverse=True
            )
            setups = sorted(
                setups_by_votes,
                key=lambda s: s.get_votes_percentage(),
                reverse=True
            )
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
        if self.request.POST:
            context['images_formset'] = SetupImageCreateFormSet(
                self.request.POST,
                self.request.FILES,
                prefix='image_fields'
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
            context['images_formset'] = SetupImageCreateFormSet(prefix='image_fields')
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

        if self.request.POST.get('car_sub_model') and self.request.POST.get('car_sub_model') is not '':
            car_sub_model_id = int(self.request.POST.get('car_sub_model'))
            form.instance.car = CarSubModel.objects.get(id=car_sub_model_id)
        elif self.request.POST.get('car_model') and self.request.POST.get('car_model') is not '':
            car_model_id = int(self.request.POST.get('car_model'))
            form.instance.car = CarModel.objects.get(id=car_model_id)
        else:
            car_brand_id = int(self.request.POST.get('car_brand'))
            form.instance.car = CarBrand.objects.get(id=car_brand_id)
        form.instance.creator = self.request.user
        self.object = form.save()

        images_formset = context['images_formset']
        engine_fields_formset = context['engine_fields_formset']
        drivetrain_fields_formset = context['drivetrain_fields_formset']
        suspension_fields_formset = context['suspension_fields_formset']
        brakes_fields_formset = context['brakes_fields_formset']
        wheels_fields_formset = context['wheels_fields_formset']
        exterior_fields_formset = context['exterior_fields_formset']
        interior_fields_formset = context['interior_fields_formset']

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

        if images_formset.is_valid():
            images_formset.instance = self.object
            for form in images_formset.ordered_forms:
                if form.cleaned_data != {} and form.cleaned_data['ORDER']:
                    form.instance.order = form.cleaned_data['ORDER']
            images_formset.save()

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SetupUpdateView(LoginRequiredMixin, UpdateView):
    model = Setup
    form_class = SetupCreateForm
    template_name = 'setup_update.html'
    slug_url_kwarg = 'setup_slug'

    def get(self, request, *args, **kwargs):
        setup = Setup.objects.get(slug=kwargs.get('setup_slug'))
        if request.user == setup.creator:
            return super(SetupUpdateView, self).get(request, *args, **kwargs)
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SetupUpdateView, self).get_context_data(**kwargs)
        context['car_brands'] = CarBrand.objects.all()
        if self.request.POST:
            context['images_formset'] = SetupImageCreateFormSet(
                self.request.POST,
                self.request.FILES,
                prefix='image_fields',
                instance=self.object,
            )
            context['engine_fields_formset'] = SetupEngineFieldCreateFormSet(
                self.request.POST,
                prefix='engine_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=0)
            )
            context['engine_fields_formset'].full_clean()
            context['drivetrain_fields_formset'] = SetupDrivetrainFieldCreateFormSet(
                self.request.POST,
                prefix='drivetrain_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=1)
            )
            context['drivetrain_fields_formset'].full_clean()
            context['suspension_fields_formset'] = SetupSuspensionFieldCreateFormSet(
                self.request.POST,
                prefix='suspension_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=2)
            )
            context['suspension_fields_formset'].full_clean()
            context['brakes_fields_formset'] = SetupBrakesFieldCreateFormSet(
                self.request.POST,
                prefix='brakes_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=3)
            )
            context['brakes_fields_formset'].full_clean()
            context['wheels_fields_formset'] = SetupWheelsFieldCreateFormSet(
                self.request.POST,
                prefix='wheels_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=4)
            )
            context['wheels_fields_formset'].full_clean()
            context['exterior_fields_formset'] = SetupExteriorFieldCreateFormSet(
                self.request.POST,
                prefix='exterior_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=5)
            )
            context['exterior_fields_formset'].full_clean()
            context['interior_fields_formset'] = SetupInteriorFieldCreateFormSet(
                self.request.POST,
                prefix='interior_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=6)
            )
            context['interior_fields_formset'].full_clean()
        else:
            context['images_formset'] = SetupImageCreateFormSet(
                prefix='image_fields',
                instance=self.object,
            )
            context['engine_fields_formset'] = SetupEngineFieldCreateFormSet(
                prefix='engine_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=0)
            )
            context['drivetrain_fields_formset'] = SetupDrivetrainFieldCreateFormSet(
                prefix='drivetrain_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=1)
            )
            context['suspension_fields_formset'] = SetupSuspensionFieldCreateFormSet(
                prefix='suspension_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=2)
            )
            context['brakes_fields_formset'] = SetupBrakesFieldCreateFormSet(
                prefix='brakes_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=3)
            )
            context['wheels_fields_formset'] = SetupWheelsFieldCreateFormSet(
                prefix='wheels_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=4)
            )
            context['exterior_fields_formset'] = SetupExteriorFieldCreateFormSet(
                prefix='exterior_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=5)
            )
            context['interior_fields_formset'] = SetupInteriorFieldCreateFormSet(
                prefix='interior_fields',
                instance=self.object,
                queryset=SetupField.objects.filter(category=6)
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()

        if self.request.POST.get('car_sub_model') and self.request.POST.get('car_sub_model') is not '':
            car_sub_model_id = int(self.request.POST.get('car_sub_model'))
            form.instance.car = CarSubModel.objects.get(id=car_sub_model_id)
        elif self.request.POST.get('car_model') and self.request.POST.get('car_model') is not '':
            car_model_id = int(self.request.POST.get('car_model'))
            form.instance.car = CarModel.objects.get(id=car_model_id)
        else:
            car_brand_id = int(self.request.POST.get('car_brand'))
            form.instance.car = CarBrand.objects.get(id=car_brand_id)
        form.instance.creator = self.request.user
        self.object = form.save()

        images_formset = context['images_formset']
        engine_fields_formset = context['engine_fields_formset']
        drivetrain_fields_formset = context['drivetrain_fields_formset']
        suspension_fields_formset = context['suspension_fields_formset']
        brakes_fields_formset = context['brakes_fields_formset']
        wheels_fields_formset = context['wheels_fields_formset']
        exterior_fields_formset = context['exterior_fields_formset']
        interior_fields_formset = context['interior_fields_formset']

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

        if images_formset.is_valid():
            images_formset.instance = self.object
            for form in images_formset.ordered_forms:
                if form.cleaned_data != {} and form.cleaned_data['ORDER']:
                    form.instance.order = form.cleaned_data['ORDER']
            images_formset.save()

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class SetupDetailView(TemplateView):
    template_name = 'setup_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SetupDetailView, self).get_context_data(**kwargs)
        context['setup'] = Setup.objects.get(slug=kwargs.get('setup_slug'))
        context['setup'].increase_views()
        if context['setup'].weight_distribution:
            context['setup_weight_distribution'] = '{0}/{1}'.format(
                context['setup'].weight_distribution,
                100 - context['setup'].weight_distribution,
            )
        return context


class SetupVoteUp(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        setup = Setup.objects.get(slug=kwargs.get('setup_slug'))
        try:
            setup_vote = SetupVote.objects.get(setup=setup, user=request.user)
            setup_vote.vote = 1
            setup_vote.save()
        except SetupVote.DoesNotExist:
            SetupVote.objects.create(setup=setup, user=request.user, vote=1)
        return JsonResponse({'vote': 'up'})


class SetupVoteDown(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        setup = Setup.objects.get(slug=kwargs.get('setup_slug'))
        print('Vote-down')
        try:
            setup_vote = SetupVote.objects.get(setup=setup, user=request.user)
            setup_vote.vote = 0
            setup_vote.save()
        except SetupVote.DoesNotExist:
            SetupVote.objects.create(setup=setup, user=request.user, vote=0)
        return JsonResponse({'vote': 'down'})
