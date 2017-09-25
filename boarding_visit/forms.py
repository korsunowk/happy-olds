from django import forms
from django.core.exceptions import ValidationError

from boarding_visit.models import BoardingVisit


class BoardingVisitForm(forms.ModelForm):
    class Meta:
        model = BoardingVisit
        fields = ['start_date', 'end_date', 'old']

    def clean_end_date(self):
        if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
            raise ValidationError('Start date must be before end date.')
        return self.cleaned_data['end_date']

    def clean_old(self):
        old = self.cleaned_data['old']
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']

        for dates in BoardingVisit.get_visits(old, excluded=self.instance):
            if dates['start'] <= start_date <= dates['end'] \
                    or dates['start'] <= end_date <= dates['end']:
                raise ValidationError('The new dates falls into the existing date range.')
        return old
