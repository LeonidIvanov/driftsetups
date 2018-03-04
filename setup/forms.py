from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Setup, SetupImage, SetupField


class SetupCreateForm(forms.ModelForm):
    class Meta:
        CAR_YEARS = ((year, str(year)) for year in range(datetime.now().year - 110, datetime.now().year)[::-1])

        model = Setup
        fields = [
            'name', 'car_year', 'engine',
            'power', 'torque', 'rev_limit',
            'weight', 'boost', 'weight_distribution',
            'description'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'name-input',
                    'placeholder': _('The HGK E92 Eurofighter')
                }
            ),
            'car_year': forms.Select(choices=CAR_YEARS, attrs={'class': 'car-years-select'}),
            'engine': forms.Select(attrs={'class': 'engine-select'}),
            'power': forms.NumberInput(
                attrs={
                    'class': 'power-input ptrw-input',
                    'placeholder': 0,
                }
            ),
            'torque': forms.NumberInput(
                attrs={
                    'class': 'torque-input ptrw-input',
                    'placeholder': 0,
                }
            ),
            'rev_limit': forms.NumberInput(
                attrs={
                    'class': 'rev-limit-input ptrw-input',
                    'placeholder': 0,
                }
            ),
            'weight': forms.NumberInput(
                attrs={
                    'class': 'weight-input ptrw-input',
                    'placeholder': 0,
                }
            ),
            'boost': forms.NumberInput(
                attrs={
                    'class': 'boost-input ptrw-input',
                    'placeholder': 0,
                }
            ),
            'weight_distribution': forms.NumberInput(
                attrs={
                    'type': 'range',
                    'class': 'range-slider',
                    'id': 'rangeSlider',
                    'min': 0,
                    'max': 100,
                }
            ),
            'description': forms.Textarea(attrs={'class': 'description-textarea'})
        }


class SetupImageCreateForm(forms.ModelForm):
    class Meta:
        model = SetupImage
        fields = ['image']
        labels = {'image': ''}
        help_texts = {'images': ''}
        widgets = {
            'image': forms.FileInput(attrs={'hidden': True})
        }


SetupImageCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupImage,
    form=SetupImageCreateForm,
    extra=0,
    can_delete=True,
    can_order=True
)


class SetupEngineFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('Mast Motorsports Mozez Canted Valve cylinder heads'),
                }
            ),
        }


SetupEngineFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupEngineFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)


class SetupDrivetrainFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('Samsonas 5-speed sequential transmission'),
                }
            )
        }


SetupDrivetrainFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupDrivetrainFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)


class SetupSuspensionFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('Front & Rear Wisefab knuckles & arms'),
                }
            )
        }


SetupSuspensionFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupSuspensionFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)


class SetupBrakesFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('Wilwood 4-piston calipers & Wilwood drilled rotors (rear)'),
                }
            )
        }


SetupBrakesFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupBrakesFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)


class SetupWheelsFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('Work Wheels L1 3P 18×9-inch (front) 18×10-inch (rear)'),
                }
            )
        }


SetupWheelsFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupWheelsFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)


class SetupExteriorFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('Complete carbon-Kevlar HGK E92 Eurofighter bodykit'),
                }
            )
        }


SetupExteriorFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupExteriorFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)


class SetupInteriorFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field']
        labels = {'field': ''}
        widgets = {
            'field': forms.TextInput(
                attrs={
                    'placeholder': _('OMP seats'),
                }
            )
        }


SetupInteriorFieldCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupField,
    form=SetupInteriorFieldCreateForm,
    extra=1,
    can_delete=False,
    can_order=False
)