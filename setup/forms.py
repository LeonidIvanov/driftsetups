from django import forms

from .models import Setup, SetupImage, SetupField


class SetupCreateForm(forms.ModelForm):
    class Meta:
        model = Setup
        fields = ['name', 'engine', 'power', 'torque', 'rev_limit', 'weight', 'description']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'name-input',
                    'placeholder': 'The HGK E92 Eurofighter'
                }
            ),
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
            'description': forms.Textarea(attrs={'class': 'description-textarea'})
        }


class SetupImageCreateForm(forms.ModelForm):
    class Meta:
        model = SetupImage
        fields = ['image', 'is_main', 'setup']
        labels = {'image': ''}
        widgets = {
            'image': forms.HiddenInput(attrs={'multiple': True}),
            'is_main': forms.HiddenInput(),
        }


SetupImageCreateFormSet = forms.inlineformset_factory(
    Setup,
    SetupImage,
    form=SetupImageCreateForm,
    extra=3,
    can_delete=False,
    can_order=False
)


class SetupEngineFieldCreateForm(forms.ModelForm):
    class Meta:
        model = SetupField
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'Mast Motorsports Mozez Canted Valve cylinder heads',
                }
            )
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
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'Samsonas 5-speed sequential transmission',
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
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'Front & Rear Wisefab knuckles & arms',
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
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'Wilwood 4-piston calipers & Wilwood drilled rotors (rear)',
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
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'Work Wheels L1 3P 18×9-inch (front) 18×10-inch (rear)',
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
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'OMP seats',
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
        fields = ['field', 'setup', 'category']
        labels = {'field': ''}
        widgets = {
            'category': forms.HiddenInput(),
            'field': forms.TextInput(
                attrs={
                    'placeholder': 'Complete carbon-Kevlar HGK E92 Eurofighter bodykit',
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