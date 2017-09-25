from django.contrib import admin

from old.models import Old
from old.forms import OldForm


@admin.register(Old)
class OldAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
    search_fields = ['id', 'first_name', 'last_name']
    form = OldForm
