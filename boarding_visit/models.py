from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from old.models import Old


class BoardingVisit(models.Model):
    old = models.ForeignKey(Old, related_name='visits')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return "{0}: {1} - {2}".format(self.old, self.start_date, self.end_date)

    @classmethod
    def get_visits(cls, old, excluded):
        """
        The class method for get list of all visits dates ranges of the Old object
        :param old: the Old model object
        :param excluded: the current visit object
        :return: the list of dates
        """
        visits = cls.objects.filter(old=old).exclude(pk=excluded.pk)

        return [{'start': vis.start_date, 'end': vis.end_date} for vis in visits]

    class Meta:
        db_table = _('boarding_visits')
        verbose_name = _('boarding visit')
        verbose_name_plural = _('boarding visits')

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(_('Start date must be before end date.'))

        old = self.old
        start_date = self.start_date
        end_date = self.end_date

        for dates in BoardingVisit.get_visits(old, excluded=self):
            if dates['start'] <= start_date <= dates['end'] \
                    or dates['start'] <= end_date <= dates['end']:
                raise ValidationError(_('The new dates falls into the existing date range.'))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.clean()
        return super(BoardingVisit, self).save(force_insert, force_update, using, update_fields)
