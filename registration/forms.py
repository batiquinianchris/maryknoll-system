from django import forms
from .models import *
from enrollment.models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class StudentForms(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'),input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y'])
    class Meta:
        model = Student
        exclude = ('student_ID','status')
        
class RegistrationForms(forms.ModelForm):
    date_enrolled = forms.DateField(initial=datetime.date.today)
    class Meta:
        model = Enrollment
        exclude = ('enrollment_ID','student_type','date_enrolled',)