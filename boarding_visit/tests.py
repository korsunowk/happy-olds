from django.test import TestCase
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

from boarding_visit.models import BoardingVisit
from old.tests import OLD_TEST_DATA, Old

from datetime import date, timedelta

# Create your tests here.


class BoardingVisitFormTest(TestCase):
    """
    The test case for BoardingVisitForm
    """
    TEST_DATE = date(year=2016, month=10, day=5)
    VALID_DATA = [
        {'old': 1, 'start_date': TEST_DATE, 'end_date': TEST_DATE + timedelta(days=3)},
        {'old': 2, 'start_date': TEST_DATE, 'end_date': TEST_DATE + timedelta(days=5)},
    ]

    def setUp(self):
        self.valid_data = self.VALID_DATA
        self.fail_data = self.valid_data

    @staticmethod
    def create_test_olds():
        """
        Test method for create test olds
        """
        for data in OLD_TEST_DATA:
            Old.objects.create(
                **data
            )

    def test_successful(self):
        """
        Simple test for successful create the new BoardingVisit objects
        """
        self.create_test_olds()

        for data in self.valid_data:
            visit = BoardingVisit.objects.create(
                **data
            )
            self.assertIsInstance(visit, BoardingVisit)
        self.assertEqual(self.valid_data.__len__(), BoardingVisit.objects.count())

    def test_fails(self):
        """
        Test error with start and end dates
        """

        self.create_test_olds()

        for data in self.valid_data:
            BoardingVisit.objects.create(
                **data
            )

        fails = 0
        for data in self.fail_data:
            try:
                BoardingVisit.objects.create(
                    **data
                )
            except ValidationError:
                fails += 1

        self.assertEqual(BoardingVisit.objects.count(), fails)


class BoardingVisitViewTest(TestCase):
    """
    The few tests for views with BoardingVisit and Old logic
    """

    def test_simple_get_homepage(self):
        """
        Simple test with GET request
        and check the 'Happy Olds' header is exist
        """
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)
        self.assertIn("Happy Olds", response.content.__str__())

    def test_send_dates_to_homepage(self):
        """
        Simple check the weekdays header when dates are sent
        """
        response = self.client.get('/',
                                   data={
                                       'start_date': '2016-09-18',
                                       'end_date': '2016-09-20'
                                   })
        self.assertEqual(200, response.status_code)
        self.assertIn("weekdays", response.content.__str__())

    def test_show_olds(self):
        """
        Test with creating the olds, visits and check
        them on the homepage with sent parameters
        """
        BoardingVisitFormTest.create_test_olds()
        visit_data = BoardingVisitFormTest.VALID_DATA

        for data in visit_data:
            BoardingVisit.objects.create(
                **data
            )

        response = self.client.get('/', data={
            'start_date': visit_data[0]['start_date'],
            'end_date': visit_data[1]['start_date']
        })
        self.assertIn(OLD_TEST_DATA[0]['first_name'], response.content.__str__())
        self.assertIn(
            "{0} {1}".format(
                OLD_TEST_DATA[0]['first_name'],
                OLD_TEST_DATA[0]['last_name']),
            response.content.__str__()
        )
        self.assertNotIn(
            "{0} {1}".format(
                OLD_TEST_DATA[2]['first_name'],
                OLD_TEST_DATA[2]['last_name']),
            response.content.__str__()
        )

    def test_generate_data(self):
        """
        Test for generate data form
        """
        data = {
            'olds_start': 5,
            'olds_end': 10,
            'visits_start': 5,
            'visits_end': 10
        }

        response = self.client.get(reverse_lazy('generate_fake_date'), data=data)
        self.assertEqual(302, response.status_code)
        self.assertNotEqual(0, Old.objects.count())
        self.assertNotEqual(0, BoardingVisit.objects.count())
