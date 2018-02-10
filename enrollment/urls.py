from django.conf.urls import url, include

from . import views

urlpatterns = [
<<<<<<< HEAD
        url(r'^$', views.index, name = 'reg-index'),
        #-----------------------CURRICULUM---------------------------------------------------------
        url(r'^curriculum-list/$', views.curriculumList, name = 'curriculum-list'),
        url(r'^curriculum-list/table$', views.tableCurriculumList, name = 'curriculum-table'),
        url(r'^curriculum-list/add$', views.addCurriculumProfile, name = 'curriculum-add'),
        url(r'^curriculum-list/create$', views.createCurriculumProfile, name = 'curriculum-create'),
        #-----------------------SECTION------------------------------------------------------------
        url(r'^section-list/$', views.sectionList, name = 'section-list'),
        #-----------------------SCHOLARSHIP--------------------------------------------------------
        url(r'^scholarship-list/$', views.scholarshipList, name = 'scholarship-list'),
        url(r'^scholarship-list/table$', views.tableScholarshipList, name = 'scholarship-table'),
        
=======
        url(r'^section/list$', views.sectionList, name = 'section-list'),
        url(r'^section/list/add$', views.addSection, name = 'section-create'),
        url(r'^section/list/add-form$', views.generateSectionForm, name = 'section-create-form'),
        url(r'^section/list/details$', views.sectionDetails, name = 'section-details'),
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80
    ]