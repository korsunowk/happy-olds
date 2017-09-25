from django.db import models
from django.utils.translation import ugettext_lazy as _

from old.models import Old


class BoardingVisit(models.Model):
    old = models.ForeignKey(Old, related_name='visits')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{0}: {1} - {2}".format(self.old, self.start_date, self.end_date)

    class Meta:
        db_table = _('boarding_visits')
        verbose_name = _('boarding visit')
        verbose_name_plural = _('boarding visits')
