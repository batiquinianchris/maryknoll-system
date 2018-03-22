from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.views import generic

from django.utils import timezone

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from .models import *
from .forms import *

from django.template.loader import render_to_string
from django.http import JsonResponse

from django.db import models
from django.http import StreamingHttpResponse
from django.views.generic import View
import csv
from cashier.models import *
from django.http import HttpResponseRedirect
from django.utils import timezone
import csv
from datetime import datetime

from .models import *
from registration.models import *
from enrollment.models import *
from cashier.models import *
from django.db.models import Q
''' USE THEM AS: reportName.as_view() IN THE URL AS THE DOWNLOAD LINK'''


class Echo(object):
    """An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
# LIST OF ENROLLED STUDENTS (WITH OLD STUDENTS)
class Enrolled_List_Report(View):
    def get(self, request, *args, **kwargs):
        
        query = Enrollment.objects.filter(~Q(get_enrollment_status_display = 'Dropped out')).filter(date_enrolled= datetime.date.today())
        file_name = 'Enrolled_List'+ str(str(datetime.date.today())) + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__str__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__str__() for item in getattr(obj, field.name).all()])
                elif field.choices:
                    val = getattr(obj, 'get_%s_display'%field.name)()
                else:
                    val = getattr(obj, field.name)
                row.append(unicode(val).encode("utf-8"))
            return row
        def stream(headers, data): # Helper function to inject headers
            if headers:
                yield headers
            for obj in data:
                yield get_row(obj)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in stream(headers, query)),
            content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="' +file_name+'"'
        return response
#LIST OF SCHOLARS
class Echo(object):
    """An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
class Scholars_List_Report(View):
    def get(self, request, *args, **kwargs):
        list_of_ids = []
        #Get enrolled students
        student_list = Student.objects.filter(status='a')
        #Get the student's latest registration
        for student in student_list:
            curr_registration = Enrollment.objects.filter(student=student).latest('date_enrolled')
            #Get scholarship list of that enrollment object
            scholar_list = StudentScholar.objects.filter(registration=curr_registration)
            #If this list exists, then the student is a scholar
            if scholar_list:
                list_of_ids.append(curr_registration.enrollment_ID)
            print(curr_registration)

        #Get list of students from the list of IDs collected
        
        scholars = Enrollment.objects.filter(enrollment_ID__in=list_of_ids)
        query = scholars
        file_name = 'Scholars_List_'+ str(str(datetime.date.today())) + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__str__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__str__() for item in getattr(obj, field.name).all()])
                elif field.choices:
                    val = getattr(obj, 'get_%s_display'%field.name)()
                else:
                    val = getattr(obj, field.name)
                row.append(unicode(val).encode("utf-8"))
            return row
        def stream(headers, data): # Helper function to inject headers
            if headers:
                yield headers
            for obj in data:
                yield get_row(obj)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in stream(headers, query)),
            content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="' +file_name+'"'
        return response
#LIST OF ALL TRANSACTIONS MADE
class Echo(object):
    """An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
class cash_reports(View):
    def get(self, request, *args, **kwargs):
        query = EnrollmentORDetails.objects.all()
        file_name = 'Cash_Reports_'+ str(str(datetime.date.today())) + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__str__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__str__() for item in getattr(obj, field.name).all()])
                elif field.choices:
                    val = getattr(obj, 'get_%s_display'%field.name)()
                else:
                    val = getattr(obj, field.name)
                row.append(unicode(val).encode("utf-8"))
            return row
        def stream(headers, data): # Helper function to inject headers
            if headers:
                yield headers
            for obj in data:
                yield get_row(obj)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in stream(headers, query)),
            content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="' +file_name+'"'
        return response

#LIST OF ALL SUBJECTS IN CURRICULUMS
class Echo(object):
    """An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
class Curriculum_Subject_List(View):
    def get(self, request, *args, **kwargs):
        query = Curriculum_Subject_List.objects.all()
        file_name = 'Curriculum_Subject_List_'+ str(datetime.date.today()) + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__str__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__str__() for item in getattr(obj, field.name).all()])
                elif field.choices:
                    val = getattr(obj, 'get_%s_display'%field.name)()
                else:
                    val = getattr(obj, field.name)
                row.append(unicode(val).encode("utf-8"))
            return row
        def stream(headers, data): # Helper function to inject headers
            if headers:
                yield headers
            for obj in data:
                yield get_row(obj)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in stream(headers, query)),
            content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="' +file_name+'"'
        return response
# All list of student profiles
class Echo(object):
    """An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value
class Export_Model_To_CSV(View):
    def get(self, request, *args, **kwargs):
        query = Student.objects.all()
        file_name = 'all_Students.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__str__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__str__() for item in getattr(obj, field.name).all()])
                elif field.choices:
                    val = getattr(obj, 'get_%s_display'%field.name)()
                else:
                    val = getattr(obj, field.name)
                row.append(unicode(val).encode("utf-8"))
            return row
        def stream(headers, data): # Helper function to inject headers
            if headers:
                yield headers
            for obj in data:
                yield get_row(obj)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse(
            (writer.writerow(row) for row in stream(headers, query)),
            content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="' +file_name+'"'
        return response