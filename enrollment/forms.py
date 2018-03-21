from django import forms
from .models import *
from registration.models import *
from enrollment.models import *

from administrative.models import *

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

from dal import autocomplete

ACTIVE = 'a'
ON_LEAVE = 'o'
INACTIVE = 'i'
STATUS_CHOICES = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive'),
)
class SectionForms(forms.ModelForm):
    teachers = Employee.objects.filter(emp_type__contains="t")
    adviser = Section.objects.filter(adviser = teachers)
    
    class Meta:
        model = Section
        exclude = ('section_ID', 'section_status',)
        
class SubjectForm(forms.ModelForm):
    """Curriculum-details-create."""

    class Meta:
        """Meta definition for Subjectform."""

        model = Subjects
        exclude = ('curriculum',)

        
class ScholarshipForms(forms.ModelForm):
    class Meta:
        model = Scholarship
        exclude = ('pk',)
        
class SubjectOfferingForms(forms.ModelForm):
    class Meta:
        model = Offering
        exclude = ('pk','school_year')

class School_YearForm(forms.ModelForm):
    """Form definition for School_Year."""

    class Meta:
        """Meta definition for School_Yearform."""

        model = School_Year
        exclude = ('date_start',)

class YearLevelForm(forms.ModelForm):
    """Form definition for School_Year."""

    class Meta:
        """Meta definition for School_Yearform."""

        model = YearLevel
        exclude = ('pk',)