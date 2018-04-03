from django.conf.urls import url, include

from . import views
from .reports_class import *

urlpatterns = [
        url(r'^$', views.index, name = 'reg-index'),
        url(r'^employee-list/$', views.userList, name = 'employee-list'),
        url(r'^employee-list/table$', views.tableEmployeeList, name = 'employee-table'),
        url(r'^employee-list/add$', views.addEmployeeProfile, name = 'employee-add'),
        url(r'^employee-list/create$', views.createEmployeeProfile, name = 'employee-create'),
        url(r'^employee-list/update/(?P<pk>\d+)$', views.updateEmployee, name = 'employee-update'),
        url(r'^employee-list/edit-form/(?P<pk>\d+)$', views.updateEmployeeForm, name = 'employee-update-form'),
    ]

urlpatterns += [
        url(r'^employee-detail/(?P<pk>\d+)$', views.employeeDetails, name = 'employee-details'),
]

#Download Links
urlpatterns += [
        url(r'^enrolled-students/$', Enrolled_List_Report.as_view(), name = 'download-enrolled'),
        url(r'^curriculum-subject/$', Curriculum_Subject_List.as_view(), name = 'download-curriculum'),
        url(r'^enrolled-scholars/$', Scholars_List_Report.as_view(), name = 'download-scholars'),
        url(r'^cash-reports/$', cash_reports.as_view(), name = 'download-cashreports'),
        url(r'^student-profiles/download$', Export_Model_To_CSV.as_view(), name = 'download-profiles'),
]