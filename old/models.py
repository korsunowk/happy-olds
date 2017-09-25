from django.db import models

# Create your models here.


class Old(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)

    @property
    def full_name(self):
        """
        The property for get full name of a model object
        :return: string with full name
        """
        if not self.last_name:
            return self.first_name

        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name
