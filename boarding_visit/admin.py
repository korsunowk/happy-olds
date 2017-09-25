from django.contrib import admin

from boarding_visit.models import BoardingVisit
from boarding_visit.forms import BoardingVisitForm


@admin.register(BoardingVisit)
class BoardingVisitAdmin(admin.ModelAdmin):
    list_display = ['old', 'start_date', 'end_date']
    list_filter = ['old', 'start_date', 'end_date']
    form = BoardingVisitForm
