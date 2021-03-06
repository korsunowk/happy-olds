from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy

from old.models import Old
from boarding_visit.models import BoardingVisit

from datetime import date, timedelta, datetime
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
    :return: redirect to homepage
    """
    fake = Faker()
    Old.objects.all().delete()
    BoardingVisit.objects.all().delete()

    olds_range = [
        int(request.GET.get('olds_start', 0)),
        int(request.GET.get('olds_end', 100))
    ]
    visits_range = [
        int(request.GET.get('visits_start', 0)),
        int(request.GET.get('visits_end', 100))
    ]

    now_year = datetime.today().year

    for _ in range(random.randint(olds_range[0], olds_range[1])):
        try:
            Old.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
        except ValidationError:
            continue

    for _ in range(random.randint(visits_range[0], visits_range[1])):
        start_date = random_date(
            start=date(year=now_year, month=1, day=1),
            end=date(year=now_year, month=12, day=31)
        )
        end_date = random_date(
            start=start_date,
            end=date(year=now_year, month=12, day=31)
        )

        try:
            BoardingVisit.objects.create(
                old_id=random.randint(Old.objects.first().pk, Old.objects.last().pk),
                start_date=start_date,
                end_date=end_date
            )
        except ValidationError:
            continue

    return redirect(to=reverse_lazy('home_page'))
