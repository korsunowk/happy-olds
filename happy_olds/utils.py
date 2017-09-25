from django.shortcuts import redirect
from django.urls import reverse_lazy

from old.models import Old
from boarding_visit.models import BoardingVisit

from datetime import date, timedelta
import random
from faker import Faker


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def generate_fake_data(request):
    """
    The method for generating randomly and fake data
    for Olds and Visits models
    :param request: django request object
    :return: HttpResponse
    """
    fake = Faker()
    Old.objects.all().delete()
    BoardingVisit.objects.all().delete()

    olds_range = []
    visits_range = []

    for _ in range(random.randint(50, 500)):
        Old.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )

    for _ in range(random.randint(50, 500)):
        old = Old.objects.get(
            pk=random.randint(Old.objects.first().pk, Old.objects.last().pk)
        )

        start_date = random_date(
            start=date(year=2016, month=1, day=1),
            end=date(year=2016, month=12, day=31)
        )
        end_date = random_date(
            start=start_date,
            end=date(year=2016, month=12, day=31)
        )

        BoardingVisit.objects.create(
            old=old,
            start_date=start_date,
            end_date=end_date
        )

    return redirect(to=reverse_lazy('home_page'))
