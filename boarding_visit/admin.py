from django.contrib import admin

from boarding_visit.models import BoardingVisit


@admin.register(BoardingVisit)
class BoardingVisitAdmin(admin.ModelAdmin):
    list_display = ['old', 'start_date', 'end_date']
    list_filter = ['old', 'start_date', 'end_date']
