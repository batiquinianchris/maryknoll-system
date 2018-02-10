from django import forms
from .models import *
<<<<<<< HEAD
from enrollment.models import *
=======
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

<<<<<<< HEAD
class CurriculumForms(forms.ModelForm):
    class Meta:
        model = Curriculum
        exclude = ('curriculum_ID',)
=======
ACTIVE = 'a'
ON_LEAVE = 'o'
INACTIVE = 'i'
STATUS_CHOICES = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive'),
)
class SectionForms(forms.ModelForm):
    section_status= forms.CharField(widget=forms.RadioSelect(choices=STATUS_CHOICES))
    class Meta:
        model = Section
        exclude = ('section_ID',)
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80
