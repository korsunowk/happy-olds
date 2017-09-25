from django.test import TestCase

from old.forms import OldForm, Old

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

    def test_success_create(self):
        """
        Test for success create of 3 Old objects
        """
        for data in self.test_data:
            form = OldForm(data=data)
            self.assertTrue(form.is_valid())
            form.save()

        self.assertEqual(self.test_data.__len__(), Old.objects.count())

    def test_fail_create(self):
        """
        Test for testings fails creating the Old objects
        """
        for data in self.test_data:
            form = OldForm(data=data)
            self.assertTrue(form.is_valid())
            form.save()

        fails = 0
        for data in self.fail_data:
            form = OldForm(data=data)

            if not form.is_valid():
                fails += 1
            self.assertFalse(form.is_valid())

        self.assertEqual(Old.objects.count(), fails)
