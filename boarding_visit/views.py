from django.views import generic
from django.db.models import Q
from django.shortcuts import render_to_response

from datetime import timedelta, datetime
from itertools import chain

from boarding_visit.models import BoardingVisit
from happy_olds import settings

# Create your views here.


class CalendarPageView(generic.TemplateView):
    template_name = 'index.html'

    WEEKDAYS = ['Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat', 'Sun']

    def get_context_data(self, **kwargs):
        context = super(CalendarPageView, self).get_context_data(**kwargs)
        context.update({
            'weekdays': self.WEEKDAYS
        })
        return context

    @staticmethod
    def get_all_visits_by_date(start_date, end_date):
        """
        Help method for get all visits in given dates range
        :param start_date: start date
        :param end_date: end date
        :return: queryset of the BoardingVisit objects
        """
        fell_in_start = lambda visit: visit.start_date <= start_date.date() <= visit.end_date
        fell_in_end = lambda visit: visit.start_date <= end_date.date() <= visit.end_date

        another_visits = [
            visit for visit in BoardingVisit.objects.all()
            if fell_in_start(visit) or fell_in_end(visit)
        ]
        visits = BoardingVisit.objects.filter(
            Q(start_date__range=[start_date.date(), end_date.date()])
            | Q(end_date__range=[start_date.date(), end_date.date()])
        ).exclude(pk__in=[obj.pk for obj in another_visits])

        visits = list(chain(another_visits, visits))
        return visits

    @staticmethod
    def get_visits_by_date(visits, date):
        """
        Help method for get visits by date in existing queryset of visits
        :param visits: the queryset of visits
        :param date: needed date
        :return: list of visits filtered by date
        """
        return [visit for visit in visits if visit.start_date <= date.date() <= visit.end_date]

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            start_date = datetime.strptime(request.GET.get('start_date'), settings.STANDARD_DATE_FORMAT)
            end_date = datetime.strptime(request.GET.get('end_date'), settings.STANDARD_DATE_FORMAT)
        except TypeError:
            return super(CalendarPageView, self).get(request, *args, **kwargs)

        context['start_date'], context["end_date"] = start_date, end_date
        context.update({
            'add_old': ''.join(
                ['http://',
                 settings.DOMAIN,
                 '/admin/olds/old/add/']
            ),
            'add_visit': ''.join(
                ['http://',
                 settings.DOMAIN,
                 '/admin/boarding_visit/boardingvisit/add/']
            )
        })

        visits = CalendarPageView.get_all_visits_by_date(start_date, end_date)
        calendar = []
        dates_range = [start_date + timedelta(days=i) for i in range(0, (end_date-start_date).days + 1)]

        # add empty days to begin of calendar
        CalendarPageView.add_to_calendar_empty_day(dates_range, calendar, index=0)

        for date in dates_range:
            calendar.append(date)

        # add empty days to end of calendar
        CalendarPageView.add_to_calendar_empty_day(dates_range, calendar, index=-1)

        calendar_with_visits = []
        for date in calendar:
            if not date:
                calendar_with_visits.append({})
                continue
            visits_by_date = CalendarPageView.get_visits_by_date(visits, date)

            calendar_with_visits.append({
                'date': date,
                'count': len(visits_by_date),
                'olds': visits_by_date
            })

        context['calendar'] = CalendarPageView.separate_dates_by_weeks(calendar_with_visits)
        return render_to_response(template_name='index.html', context=context)

    @staticmethod
    def add_to_calendar_empty_day(dates_range, calendar, index=0):
        """
        Help method for add empty days before start day to calendar
        for example: if start_day is Tuesday then add empty day for Mon

        :param dates_range: range with dates
        :param index: index of object in dates_range
        :param calendar: calendar object with all dates (with empty days)
        """
        col = dates_range[index].weekday() if index == 0 else 7 - dates_range[index].weekday()
        for _ in range(col):
            calendar.append(None)

    @staticmethod
    def separate_dates_by_weeks(calendar):
        """
        Help method for separate all given dates by weeks
        :param calendar: the list of dates
        :return: the new list with weeks
        """
        output_calendar = []
        i = 0
        for date in range(int(len(calendar) / 7)):
            output_calendar.append(calendar[i:i+7])
            i += 7

        return output_calendar
