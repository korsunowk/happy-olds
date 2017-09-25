from django import forms
from django.core.exceptions import ValidationError

from old.models import Old
from old.utils import full_name_check


class OldForm(forms.ModelForm):
    class Meta:
        model = Old
        fields = ['first_name', 'last_name']

    def clean(self):
        valid_name = full_name_check(self.cleaned_data)
        if not valid_name:
            raise ValidationError('Full name of the Old must be unique.')
