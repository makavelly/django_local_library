from django.test import TestCase
import datetime
from django.utils import timezone
from catalog.forms import RenewBookForm

class RenewBookFormTest(TestCase):

	def test_renew_form_date_field_label(self):
		form = RenewBookForm()        
		self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

	def test_renew_form_date_field_help_text(self):
		form = RenewBookForm()
		self.assertEqual(form.fields['renewal_date'].help_text,'Enter a date between now and 4 weeks (default 3).')
