from django.conf.urls import url, include

from . import views

urlpatterns = [
        url(r'^$', views.index, name = 'reg-index'),
        url(r'^student-list/$', views.registrationList, name = 'student-list'),
        url(r'^student-list/table$', views.tableStudentList, name = 'student-table'),
        url(r'^student-list/add$', views.addStudentProfile, name = 'student-add'),
        url(r'^student-list/create$', views.createStudentProfile, name = 'student-create'),
        url(r'^student-list/search$', views.searchStudent, name = 'student-search'),  
        #student profile urls
        url(r'^student-list/(?P<pk>\d+)$', views.studentDetails, name = 'student-details'),
        url(r'^student-list/enrollment-table/(?P<pk>\d+)$', views.tableEnrollmentList, name = 'enrollment-table'),
        url(r'^student-list/enrollment-add/(?P<pk>\d+)$', views.addEnrollment, name = 'enrollment-add'),
        url(r'^student-list/enrollment-create/(?P<pk>\d+)$', views.createEnrollment, name = 'enrollment-create'),
        #url(r'^student-list/enrollment-create/sort(?P<pk>\d+)$', views.sortSections, name = 'sort-sections'),
    ]