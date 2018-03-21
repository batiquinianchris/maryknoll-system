from django.shortcuts import render, get_object_or_404
from django.views import generic

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
        query = Enrollment.objects.filter(~Q(enrollment_status = 'd'))
        file_name = 'Enrolled_List'+ datetime.date.today() + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__unicode__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
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
                list_of_ids.append(student.student_ID)
        #Get list of students from the list of IDs collected
        scholars = Student.objects.filter(student_ID__in=list_of_ids)
        query = scholars
        file_name = 'Scholars_List'+ datetime.date.today() + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__unicode__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
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
class cash_reports(View):
    def get(self, request, *args, **kwargs):
        query = EnrollmentORDetails.objects.all()
        file_name = 'Cash_Reports_'+ datetime.date.today() + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__unicode__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
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
class Curriculum_Subject_List(View):
    def get(self, request, *args, **kwargs):
        query = Curriculum_Subject_List.objects.all()
        file_name = 'Curriculum_Subject_List'+ datetime.date.today() + '.csv'
        model = query.model
        model_fields = model._meta.fields + model._meta.many_to_many
        headers = [field.name for field in model_fields] # Create CSV headers
        def get_row(obj):
            row = []
            for field in model_fields:
                if type(field) == models.ForeignKey:
                    val = getattr(obj, field.name)
                    if val:
                        val = val.__unicode__()
                elif type(field) == models.ManyToManyField:
                    val = u', '.join([item.__unicode__() for item in getattr(obj, field.name).all()])
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