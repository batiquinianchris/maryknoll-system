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

#Download Links
urlpatterns += [
        url(r'^enrolled-students/$', Enrolled_List_Report.as_view(), name = 'download-enrolled'),
]