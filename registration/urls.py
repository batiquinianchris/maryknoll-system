from django.conf.urls import url, include
from .models import *
from .views import *

urlpatterns = [
        url(r'^student-list/$', studentList, name = 'student-list'),
        url(r'^student-list/table$', table_StudentList, name = 'student-table'),
        url(r'^student-list/table-active$', table_ActiveList, name = 'student-table-active'),
        url(r'^student-list/table-inactive$', table_InActiveList, name = 'student-table-inactive'),
        url(r'^student-list/table-scholars$', table_ScholarList, name = 'student-table-scholars'),
        url(r'^student-list/add$', addStudent, name = 'student-add'),
        url(r'^student-list/create$', form_addStudent, name = 'student-create'),
        url(r'^student-list/update/(?P<pk>\d+)$', updateStudentProfile, name = 'student-update'),
        url(r'^student-list/edit-form/(?P<pk>\d+)$', form_updateStudentProfile, name = 'student-edit-form'),
        #student profile urls
        url(r'^student-list/(?P<pk>\d+)$', studentDetails, name = 'student-details'),
        url(r'^student-list/enrollment-table/(?P<pk>\d+)$', table_studentDetails, name = 'enrollment-table'),
        url(r'^student-list/enrollment-add/(?P<pk>\d+)$', addEnrollment, name = 'enrollment-add'),
        url(r'^student-list/enrollment-create/(?P<pk>\d+)$', form_addEnrollment, name = 'enrollment-create'),
        url(r'^student-list/enrollment-edit/(?P<pk>\d+)$', editEnrollment, name = 'enrollment-edit'),
        url(r'^student-list/enrollment-edit-form/(?P<pk>\d+)$', form_editEnrollment, name = 'enrollment-edit-form'),
        #url(r'^student-list/enrollment-create/sort(?P<pk>\d+)$', sortSections, name = 'sort-sections'),
        url(r'^scholarship-table/(?P<pk>\d+)$', table_studentScholar, name='student-scholars-table'),
        url(r'^scholarship-delete/$', deleteScholar, name='delete-scholar'),
        url(r'^scholarship-add/(?P<pk>\d+)$', StudentScholarFormView, name='student-scholars-add'),
        url(r'^transaction-logs/(?P<pk>\d+)$', tableTransactionLogs , name='student-transaction-log'),
        url(r'^subjects-table/(?P<pk>\d+)$', subjectsView , name='subjects-table'),
    ]