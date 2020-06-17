from django.test import SimpleTestCase
from routeplanner.forms import leapCardForm

class TestForms(SimpleTestCase):

    def test_leapCardForm(self):
        form = leapCardForm(data={
            'username':'123',
            'password':'321'
        })

        self.assertTrue(form.is_valid())

    def test__leapCardForm_no_data(self):
        form = leapCardForm(data={
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
