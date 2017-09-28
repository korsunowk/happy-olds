from django.test import TestCase
from django.core.exceptions import ValidationError

from old.models import Old

# Create your tests here.

OLD_TEST_DATA = [
    {'first_name': 'Peter', 'last_name': 'German'},
    {'first_name': 'Michael', 'last_name': ''},
    {'first_name': 'Michael', 'last_name': 'Peter'}
]


class OldModelTest(TestCase):
    """
    TestCase for the Old model
    """
    def setUp(self):
        self.test_data = OLD_TEST_DATA

        self.fail_data = self.test_data

        for data in self.test_data:
            old = Old.objects.create(
                **data
            )
            self.assertIsInstance(old, Old)

    def test_count___old_after_setup__must_3(self):
        """
        Test for get count of Olds objects after the setUp method
        """
        self.assertEqual(self.test_data.__len__(), Old.objects.count())

    def test_create_olds_with_the_same_names__must_3_errors(self):
        """
        Test for testings fails creating the Old objects
        """
        fails = 0
        for data in self.fail_data:
            try:
                old = Old.objects.create(
                    **data
                )
                self.assertIsInstance(old, Old)
            except ValidationError:
                fails += 1

        self.assertEqual(Old.objects.count(), fails)
