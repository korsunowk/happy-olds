from django.shortcuts import redirect
from django.urls import reverse_lazy

from old.forms import Old, OldForm
from boarding_visit.forms import BoardingVisit, BoardingVisitForm

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
    :return: HttpResponse
    """
    fake = Faker()
    Old.objects.all().delete()
    BoardingVisit.objects.all().delete()

    olds_range = []
    visits_range = []

    now_year = datetime.today().year

    for _ in range(random.randint(50, 500)):
        form = OldForm(data=dict(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        ))

        if form.is_valid():
            form.save()

    for _ in range(random.randint(50, 500)):
        old = Old.objects.get(
            pk=random.randint(Old.objects.first().pk, Old.objects.last().pk)
        )

        start_date = random_date(
            start=date(year=now_year, month=1, day=1),
            end=date(year=now_year, month=12, day=31)
        )
        end_date = random_date(
            start=start_date,
            end=date(year=now_year, month=12, day=31)
        )

        form = BoardingVisitForm(data=dict(
            old=old,
            start_date=start_date,
            end_date=end_date
        ))

        if form.is_valid():
            form.save()

    return redirect(to=reverse_lazy('home_page'))
