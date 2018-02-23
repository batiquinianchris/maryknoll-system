from django.conf.urls import url, include

from . import views

urlpatterns = [
        url(r'^section/list/details$', views.sectionDetails, name = 'section-details'),
        url(r'^$', views.index, name = 'reg-index'),
        #-----------------------CURRICULUM---------------------------------------------------------
        url(r'^curriculum-list/$', views.curriculumList, name = 'curriculum-list'),
        url(r'^curriculum-list/table$', views.tableCurriculumList, name = 'curriculum-table'),
        url(r'^curriculum-list/add$', views.addCurriculumProfile, name = 'curriculum-add'),
        url(r'^curriculum-list/create$', views.createCurriculumProfile, name = 'curriculum-create'),
        #-----------------------SECTION------------------------------------------------------------
        url(r'^section/list$', views.sectionList, name = 'section-list'),
        url(r'^section/list/table$', views.sectionTable, name = 'section-table'),
        url(r'^section/list/add$', views.addSection, name = 'section-create'),
        #url(r'^section/list/detail$', views.detailSection, name = 'section-create'),
        url(r'^section/list/add-form$', views.generateSectionForm, name = 'section-create-form'),
        #-----------------------SCHOLARSHIP--------------------------------------------------------
        url(r'^scholarship-list/$', views.scholarshipList, name = 'scholarship-list'),
        url(r'^scholarship-list/table$', views.tableScholarshipList, name = 'scholarship-table'),
        url(r'^scholarship-list/add$', views.addScholarshipProfile, name = 'scholarship-add'),
        url(r'^scholarship-list/create$', views.createScholarshipProfile, name = 'scholarship-create'),
        #-----------------------SUBJECT OFFERING----------------------------------------------------
        url(r'^subjectOffering-list/$', views.subjectOfferingList, name = 'subjectOffering-list'),
        url(r'^subjectOffering-list/table$', views.tableSubjectOfferingList, name = 'subjectOffering-table'),
        url(r'^subjectOffering-list/add$', views.addSubjectOfferingProfile, name = 'subjectOffering-add'),
        url(r'^subjectOffering-list/create$', views.createSubjectOfferingProfile, name = 'subjectOffering-create'),
        
        
    ]