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

    @classmethod
    def full_name_check(cls, old_name):
        """
        The class method for check the unique full_name of a Old model
        :param old_name: the dict with first/last name of the Old object
        :return: True if free, False if already exists
        """
        return not cls.objects.filter(**old_name).exists()

    def __str__(self):
        return self.full_name
