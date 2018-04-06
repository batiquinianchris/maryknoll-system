from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
# Create your views here.
from .models import *
from registration.models import *
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse

# Global Functions -- Applicable to other modules

@login_required
def index(request):
    pass

def ajaxTable(request, template, context, data = None):
    # For templates that needs ajax
    html_form = render_to_string(template,
        context,
        request = request,
    )
    if data:
        data['html_form'] = html_form
    else:
        data = {'html_form' : html_form}
    return JsonResponse(data)
def updateInstance(request, modelForm, instance):
    if request.method == 'POST':
        form = modelForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
    else:
        form = modelForm(instance = instance)
    return form
def getLatest(model, attribute):
    # Get latest record of a model, basing on a certain attribute
    # Returns an instance
    try:
        latest = model.objects.latest(attribute)
    except:
        latest = None
    return latest
def paginateThis(request, obj_list, num):
    # Pagination. Send request, the list you want to paginate, and number of items per page.
    # This returns a limited list with pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(obj_list, num)
    try:
        lists = paginator.page(page)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)
    return lists
# Custom Functions - Only for this module
def getSectionList(request):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Section.objects.filter(
                Q(section_ID__contains=search)|
                Q(section_name__icontains=search)|
                Q(section_capacity__contains=search)|
                Q(adviser__first_name__icontains=search)|
                Q(adviser__last_name__icontains=search)|
                Q(room__icontains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Section.objects.filter(
                Q(section_ID__contains=search)|
                Q(section_name__icontains=search)|
                Q(section_capacity__contains=search)|
                Q(adviser__icontains=search)|
                Q(room__icontains=search)
            )
        elif(genre == "Section ID"):
            print "id"
            query = Section.objects.filter(section_ID__contains=search)
        elif(genre == "Section Name"):
            query = Section.objects.filter(section_name__icontains=search)
        elif(genre == "Room"):
            query = Section.objects.filter(room__icontains=search)
        elif(genre == "Adviser"):
            query = Section.objects.filter(Q(adviser__first_name__icontains=search)|
                Q(adviser__last_name__icontains=search))
        else:
            print "wala"
            query = Section.objects.all() 
            
    else:
        return []
    return query
def getScholarshipList(request):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Scholarship.objects.filter(
                Q(pk__contains=search)|
                Q(scholarship_name__icontains=search)|
                Q(school_year__contains=search)|
                Q(scholarship_type__icontains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Scholarship.objects.filter(
                Q(pk__contains=search)|
                Q(scholarship_name__icontains=search)|
                Q(school_year__contains=search)|
                Q(scholarship_type__icontains=search)
            )
        elif(genre == "Scholarship ID"):
            print "id"
            query = Scholarship.objects.filter(pk__contains=search)
        elif(genre == "Scholarship Name"):
            query = Scholarship.objects.filter(scholarship_name__icontains=search)
        elif(genre == "Validity"):
            query = Scholarship.objects.filter(school_year__icontains=search)
        elif(genre == "Scholarship Type"):
            query = Scholarship.objects.filter(scholarship_type__icontains=search)
        else:
            print "wala"
            query = Scholarship.objects.all()
            
    else:
        return []
    return query
def getOfferingList(request, pk):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Offering.objects.filter(
                Q(offering_ID__contains=search)|
                Q(subject__subject_name__icontains=search)|
                Q(teacher__first_name__icontains==search)|
                Q(teacher__last_name__icontains==search)|
                Q(section__section_name__icontains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Offering.objects.filter(
                Q(offering_ID__contains=search)|
                Q(subject__subject_name__icontains=search)|
                Q(teacher__first_name__icontains==search)|
                Q(teacher__first_name__icontains==search)|
                Q(section__section_name__icontains=search)
            )
        elif(genre == "Offering ID"):
            print "id"
            query = Offering.objects.filter(offering_ID__contains=search)
        elif(genre == "Subject Description"):
            query = Offering.objects.filter(subject__subject_name__icontains=search)
        elif(genre == "Teacher Assigned"):
            query = Offering.objects.filter( Q(teacher__first_name__icontains==search)|
                Q(teacher__last_name__icontains==search))
        elif(genre == "Section Assigned"):
            query = Offering.objects.filter(section__section_name__icontains=search)
        else:
            print "wala"
            query = Offering.objects.all() 
            
    else:
        return []
    return query

''' VIEWS FOR ENROLLMENT MODULE '''

#--------------------------------------CURRICULUM------------------------------------------------------
@login_required
def curriculumList(request, template = 'enrollment/curriculum/curriculum-list.html'):
    '''simple error handling: if current year is == year of latest curriculum created, disable the button'''
    disabled = False
    try:
        latest_curr = Curriculum.objects.latest('curriculum_year')
        if datetime.today().year == latest_curr.get_year():
            disabled = True
    except:
        latest_curr = None
        disabled = False
    context = {'disabled':disabled}
    return render(request, template, context)

#this function initiates a new curriculum
def addCurriculumProfile(request):
    #This simply adds a new curriculum to the database
    new_curriculum = Curriculum(curriculum_status='Active')
    new_curriculum.save()
    data = {'form_is_valid' : True }
    return JsonResponse(data)

def openCurriculumSubjectAdd(request, pk='pk', template = 'enrollment/curriculum/curriculum-list-add.html' ):
    curriculum = Curriculum.objects.get(curriculum_ID=pk)
    context = {'curriculum':curriculum}
    return render(request, template, context)

def tableCurriculumList(request, template = 'enrollment/curriculum/table-curriculum-list.html'):
    curriculum_list = Curriculum.objects.all()
    curriculum = paginateThis(request,curriculum_list, 10)
        
    context = {'curriculum_list': curriculum}
    
    return ajaxTable(request,template,context)

def createCurriculumProfile(request, pk, template = 'enrollment/curriculum/forms-curriculum-subjects-list-create.html'):
    curr = Curriculum.objects.get(curriculum_ID = pk)
    data = {'form_is_valid' : False }

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.curriculum = curr
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SubjectForm()
    context = {'form': form, 'curriculum':curr}
    return ajaxTable(request,template,context,data)
    
def curriculumDetails(request, pk='pk', template = 'enrollment/curriculum/curriculum-subjects-list.html'):
    curriculum = get_object_or_404(Curriculum, curriculum_ID=pk)
    try:
        last_record = Subjects.objects.filter(curriculum=curriculum).latest('enrollment_ID')
    except:
        last_record = Subjects.objects.filter(curriculum=curriculum)

    context = {'curriculum': curriculum, 'record':last_record}
    return render(request, template, context)
    
def tableCurriculumSubjectList(request, pk='pk', template='enrollment/curriculum/table-curriculum-subject-list.html'):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    subject_list = Subjects.objects.filter(curriculum = curriculum)
    
    subjects = paginateThis(request, subject_list, 10)
    context = {'subject_list': subjects, "curriculum": curriculum}
    return ajaxTable(request,template,context)

def editSubject(request, pk='pk', template = 'enrollment/curriculum/curriculum-subjects-list-update.html'):
    subject = get_object_or_404(Subjects, pk=pk)
    curriculum = subject.curriculum
    context = {'subject':subject, 'curriculum':curriculum}
    return render(request, template, context)
    
def form_editSubject(request, pk='pk', template = 'enrollment/curriculum/forms-curriculum-subjects-list-edit.html'):
    instance = get_object_or_404(Subjects, subject_ID=pk)
    data = {'form_is_valid' : False }
    curriculum = instance.curriculum
    

    forms = updateInstance(request, SubjectForm, instance)

    if forms.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False
    context = {'form': forms, 'curriculum':curriculum, 'instance': instance}
    return ajaxTable(request,template,context,data)
    
#--------------------------------------SECTION--------------------------------------------------------
def sectionList(request, template = 'enrollment/section/section-list.html'):
    return render(request, template)
    
def addSection(request, template = 'enrollment/section/section-list-add.html'):
    return render(request, template)
    
def sectionTable(request, template = 'enrollment/section/table-section-list.html'):
    section_list = getSectionList(request)
    section = paginateThis(request,section_list, 6)
    context = {'section_list': section}
    return ajaxTable(request,template,context)
    
def sectionDetails(request, pk='pk', template = 'enrollment/section/section-details.html'):
    section = get_object_or_404(Section, pk=pk)
    context = {'section': section}
    return render(request, template, context)
    
def tableSectionDetail(request, pk='pk',template='enrollment/section/table-section-details.html'):
    section = get_object_or_404(Section, pk=pk)
    section_enrollee_list = Enrollment.objects.filter(section = section)
    section_page = paginateThis(request, section_enrollee_list, 50)

    context = {'section_enrollee_list': section_page}
    
    html_form = render_to_string(template, context, request = request,)
    return JsonResponse({'html_form' : html_form})

def sectionDetailAdd(request, pk='pk'):
    print "wan"
    return ajaxTable(request,template,context)

def sectionDetailAdd(request, pk='pk', template = 'enrollment/section/section-details-add.html'):
    section = get_object_or_404(Section, pk=pk)
    context = {'section': section}
    return render(request, template, context)
    
def sectionDetailForm(request,pk,template='enrollment/section/forms-section-detail-create.html'):
    section = get_object_or_404(Section, pk=pk)
    students = Enrollment.objects.all()
    context = {'section': section,'student_list':students}
    data = {}
    data['form_is_valid'] = False
    if request.method == 'POST':
        student_ID = request.POST.get('student_ID')
        student = Enrollment.objects.get(pk=student_ID)
        student.section = section
        student.save()
        data['form_is_valid'] = True

    return ajaxTable(request,template,context,data)

def studentNames(request,template="enrollment/section/student-details.html"):
    registration_ID = request.GET.get('student')
    try:
        student = Enrollment.objects.get(pk=registration_ID)
    except:
        student = None
    context = {'student':student}
    return ajaxTable(request,template,context)
    
def getSectionList(request):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(genre == "Category"):
        genre = "All categories"
    
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Section.objects.filter(
                Q(section_ID__icontains=search)|
                Q(room__icontains=search)|
                Q(section_name__icontains=search)|
                Q(section_capacity__icontains=search)|
                Q(adviser__first_name__icontains=search)|
                Q(adviser__last_name__icontains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Section.objects.filter(
                Q(section_ID__icontains=search)|
                Q(room__icontains=search)|
                Q(section_name__icontains=search)|
                Q(section_capacity__icontains=search)|
                Q(adviser__first_name__icontains=search)|
                Q(adviser__last_name__icontains=search)
            )
        elif(genre == "Section ID"):
            print "id"
            query = Section.objects.filter(section_ID__icontains=search)
        elif(genre == "Section Name"):
            query = Section.objects.filter(section_name__icontains=search)
        elif(genre == "Room"):
            query = Section.objects.filter(room__icontains=search)
        elif(genre == "Adviser"):
            query = Section.objects.filter(Q(adviser__first_name__icontains=search)|
                Q(adviser__last_name__icontains=search))
        else:
            print "wala"
            query = Section.objects.all() 
        print genre
        print isNum
    elif(request.GET.get('search') == "None"):
        query = Section.objects.all()
    else:
        return []
    return query
    
def generateSectionForm(request):
    student = None
    context = {'student':student}
    return ajaxTable(request,template,context)

def generateSectionForm(request,template='enrollment/section/forms-section-create.html'):

    data = {'form_is_valid' : False }
    last_section = getLatest(Section,'section_ID')
   
    if request.method == 'POST':
        form = SectionForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.section_status = 'a'
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SectionForms()
    context = {'forms': form, 'section':last_section}
    return ajaxTable(request,template,context,data)

def editSection(request, pk='pk',template = 'enrollment/section/section-list-update.html'):
    instance = get_object_or_404(Section, pk=pk)
    context = {'instance': instance}
    return render(request, template, context)
    
def form_editSection(request, pk='pk', template = 'enrollment/section/forms-section-edit.html'):
    instance = get_object_or_404(Section, pk=pk)
    data = {'form_is_valid' : False }
    last_section = getLatest(Section,'section_ID')

    forms = updateInstance(request, SectionForms, instance)

    if forms.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    context = {'forms': forms, 'section':last_section, 'instance': instance}
    return ajaxTable(request,template,context,data)
    

#--------------------------------------SCHOLARSHIP----------------------------------------------------
@login_required
def scholarshipList(request, template = 'enrollment/scholarship/scholarship-list.html'):
    return render(request, template)

def addScholarshipProfile(request, template = 'enrollment/scholarship/scholarship-list-add.html'):
    return render(request, template)
    
def tableScholarshipList(request, template = 'enrollment/scholarship/table-scholarship-list.html'):
    schoolyear_list = getScholarshipList(request)
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(schoolyear_list, 5)
    
    try:
        scholarship = paginator.page(page)
    except PageNotAnInteger:
        scholarship = paginator.page(1)
    except EmptyPage:
        scholarship = paginator.page(paginator.num_pages)
    context = {'scholarship_list': scholarship}
    html_form = render_to_string('enrollment/table-scholarship-list.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})

def getScholarshipList(request):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Scholarship.objects.filter(
                Q(pk__icontains=search)|
                Q(scholarship_name__icontains=search)|
                Q(school_year__icontains=search)|
                Q(scholarship_type__icontains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Scholarship.objects.filter(
                Q(pk__icontains=search)|
                Q(scholarship_name__icontains=search)|
                Q(school_year__icontains=search)|
                Q(scholarship_type__icontains=search)
            )
        elif(genre == "Scholarship ID"):
            print "id"
            query = Scholarship.objects.filter(pk__icontains=search)
        elif(genre == "Scholarship Name"):
            query = Scholarship.objects.filter(scholarship_name__icontains=search)
        elif(genre == "Validity"):
            query = Scholarship.objects.filter(school_year__icontains=search)
        elif(genre == "Scholarship Type"):
            query = Scholarship.objects.filter(scholarship_type__icontains=search)
        else:
            print "wala"
            query = Scholarship.objects.all()
            
    else:
        return []
    return query
    scholarship = paginateThis(request, schoolyear_list, 5)
        
    context = {'scholarship_list': scholarship}
    return ajaxTable(request,template,context)

def createScholarshipProfile(request, template = 'enrollment/scholarship/forms-scholarship-create.html'):
    data = {'form_is_valid' : False }
    try:
        last_scholarship = Scholarship.objects.latest('scholarship_ID')
    except:
        last_scholarship = None
    if request.method == 'POST':
        form = ScholarshipForms(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            print form.errors
            data['form_is_valid'] = False
    else:
        form = ScholarshipForms()
    context = {'form': form, 'scholarship':last_scholarship}
    return ajaxTable(request,template,context,data)
    
def updateScholarship(request, pk='pk',template = 'enrollment/scholarship/scholarship-list-update.html'):
    instance = get_object_or_404(Scholarship, pk=pk)
    context = {'instance': instance}
    return render(request, template,context)


def editScholarshipForm(request, pk='pk', template = 'enrollment/scholarship/forms-scholarship-edit.html'):
    instance = get_object_or_404(Scholarship, pk=pk)
    data = {'form_is_valid' : False }
    try:
        last_scholarship = Scholarship.objects.latest('scholarship_ID')
    except:
        last_scholarship = None
    if request.method == 'POST':
        form = ScholarshipForms(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = ScholarshipForms(instance = instance)
    context = {'form': form, 'scholarship':last_scholarship, 'instance': instance}
    return ajaxTable(request,template,context,data)

def scholarList(request, pk, template='enrollment/scholarship/scholarship-details-list.html'):
    scholarship = Scholarship.objects.get(pk=pk)
    context = {'scholarship':scholarship}
    return render(request,template,context) 

def scholarTable(request,pk,template='enrollment/scholarship/table-scholarship-details-list.html'):
    scholarship = Scholarship.objects.get(pk=pk)
    context = {'scholarship':scholarship}
    return ajaxTable(request,template,context)


#--------------------------------------SUBJECT OFFERING------------------------------------------------
@login_required
def subjectOfferingList(request, pk='pk', template='enrollment/subject-offering/subject-offering.html'):
    school_year = School_Year.objects.get(pk=pk)
    context = {'school_year': school_year}
    return render(request, template, context)
    
def addSubjectOfferingProfile(request, pk, template='enrollment/subject-offering/subject-offering-add.html'):
    school_year = School_Year.objects.get(id=pk)
    context= {'school_year':school_year}
    return render(request, template,context)
    
def tableSubjectOfferingList(request, pk,template = 'enrollment/subject-offering/table-subject-offering.html'):
    sy = School_Year.objects.get(id=pk)
    subjectOffering_list = getOfferingList(request, sy.pk)
    subjectOffering = paginateThis(request,subjectOffering_list,10)

    context = {'subjectOffering_list': subjectOffering}
    return ajaxTable(request,template,context)

def createSubjectOfferingProfile(request, pk, template = 'enrollment/subject-offering/forms-subject-offering-create.html'):
    curr_sy = School_Year.objects.get(id=pk)
    data = {'form_is_valid' : False }
    try:
        last_subjectOffering = SubjectOffering.objects.latest('subjectOffering_ID')
    except:
        last_subjectOffering = None
    if request.method == 'POST':
        form = SubjectOfferingForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.school_year = curr_sy
            post.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SubjectOfferingForms()
    context = {'form': form, 'subjectOffering':last_subjectOffering, 'school_year': curr_sy}
    return ajaxTable(request,template,context,data)
    
def subjectOfferingDetail(request, pk='pk', template = 'enrollment/subject-offering/subject-offering-add.html.html'):
    subjOffering = get_object_or_404(Student, pk=pk)
    try:
        last_record = Enrollment.objects.filter(subjOffering=subjOffering).latest('enrollment_ID')
    except:
        last_record = Enrollment.objects.filter(subjOffering=subjOffering)
    context = {'subjOffering': subjOffering, 'record':last_record}
    return render(request, template, context)
    


def updateSubjectOffering(request, pk='pk', template='enrollment/subject-offering/subject-offering-update.html'):
    instance = get_object_or_404(Offering, pk=pk)
    context = {'instance': instance, 'school_year':instance.school_year}
    return render(request, template, context)

def editSubjectOfferingForm(request, pk='pk',template = 'enrollment/subject-offering/forms-subject-offering-edit.html'):
    instance = get_object_or_404(Offering, pk=pk)
    data = {'form_is_valid' : False }
    last_subjectOffering = getLatest(Offering, 'subjectOffering_ID')
    forms = updateInstance(request, SubjectOfferingForms, instance)

def getOfferingList(request, pk):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Offering.objects.filter(
                Q(offering_ID__icontains=search)|
                Q(subject__subject_name__icontains=search)|
                Q(teacher__first_name__icontains==search)|
                Q(teacher__last_name__icontains==search)|
                Q(section__section_name__icontains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Offering.objects.filter(
                Q(offering_ID__icontains=search)|
                Q(subject__subject_name__icontains=search)|
                Q(teacher__first_name__icontains==search)|
                Q(teacher__first_name__icontains==search)|
                Q(section__section_name__icontains=search)
            )
        elif(genre == "Offering ID"):
            print "id"
            query = Offering.objects.filter(offering_ID__icontains=search)
        elif(genre == "Subject Description"):
            query = Offering.objects.filter(subject__subject_name__icontains=search)
        elif(genre == "Teacher Assigned"):
            query = Offering.objects.filter( Q(teacher__first_name__icontains==search)|
                Q(teacher__last_name__icontains==search))
        elif(genre == "Section Assigned"):
            query = Offering.objects.filter(section__section_name__icontains=search)
        else:
            print "wala"
            query = Offering.objects.all() 
           
    if forms.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False
    
    context = {'form': forms, 'subjectOffering':last_subjectOffering, 'instance': instance, 'school_year': instance.school_year}
    return ajaxTable(request,template,context,data)

    
#--------------------------------------SCHOOL YEAR------------------------------------------------

def schoolYearList(request, template='enrollment/school-year/schoolyear-list.html'):
    return render(request,template)

def tableSchoolYearList(request,template='enrollment/school-year/table-schoolyear-list.html'):
    schoolyear_list = School_Year.objects.all()
    school_year = paginateThis(request,schoolyear_list, 5)
    
    context = {'schoolyear_list': school_year}
    return ajaxTable(request,template,context)
    
def createSchoolYear(request, template='enrollment/school-year/schoolyear-list-add.html'):
    return render(request,template)

def form_createSchoolYear(request,template='enrollment/school-year/forms-schoolyear-create.html'):
    data = {'form_is_valid' : False }
    last_schoolYear = getLatest(School_Year, School_Year._meta.pk)
    
    if request.method == 'POST':
        form = School_YearForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = School_YearForm()
    context = {'forms': form, 'schoolYear':last_schoolYear}
    return ajaxTable(request,template,context,data)

def editSchoolYear(request, pk='pk',template = 'enrollment/school-year/schoolyear-list-update.html'):
    instance = get_object_or_404(School_Year, pk=pk)
    context = {'instance': instance}
    return render(request, template, context)
    
def form_editSchoolYear(request, pk='pk', template = 'enrollment/school-year/forms-schoolyear-edit.html'):
    instance = get_object_or_404(School_Year, pk=pk)
    data = {'form_is_valid' : False }
    last_school_year = getLatest(School_Year, School_Year._meta.pk)

    forms = updateInstance(request, School_YearForm, instance)

    if forms.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    context = {'forms': forms, 'school_year':last_school_year, 'instance': instance}
    return ajaxTable(request,template,context,data)

def delete_schoolYear(request, pk='pk'):
    instance = get_object_or_404(School_Year, pk=pk)
    instance.delete()
    message.success(request, "Deleted!")
    return redirect('enrollment:schoolyear-list')

#--------------------------------------YEAR LEVEL------------------------------------------------

def yearLevelList(request,template='enrollment/year-level/year-level-list.html'):
    return render(request,template)

def tableYearLevelList(request,template='enrollment/year-level/table-year-level-list.html'):
    yearlevel_list = YearLevel.objects.all()
    year_level = paginateThis(request,yearlevel_list,10)
    
    context = {'yearlevel_list': year_level}
    return ajaxTable(request,template,context)

def createYearLevel(request,template='enrollment/year-level/year-level-list-add.html'):
    return render(request,template)

def form_createYearLevel(request,template='enrollment/year-level/forms-year-level-create.html'):
    data = {'form_is_valid' : False }
    last_schoolYear = getLatest(YearLevel, YearLevel._meta.pk)
    
    if request.method == 'POST':
        form = YearLevelForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = YearLevelForm()
    context = {'forms': form, 'schoolYear':last_schoolYear}
    return ajaxTable(request,template,context,data)
    
def editYearLevel(request, pk='pk',template = 'enrollment/year-level/year-level-list-update.html'):
    instance = get_object_or_404(YearLevel, pk=pk)
    context = {'instance': instance}
    return render(request, template, context)
    
def form_editYearLevel(request, pk='pk', template = 'enrollment/year-level/forms-year-level-edit.html'):
    instance = get_object_or_404(YearLevel, pk=pk)
    data = {'form_is_valid' : False }
    last_year_level = getLatest(YearLevel, YearLevel._meta.pk)

    forms = updateInstance(request, YearLevelForm, instance)

    if forms.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    context = {'forms': forms, 'year_level':last_year_level, 'instance': instance}
    return ajaxTable(request,template,context,data)

def delete_yearLevel(request, pk='pk'):
    instance = get_object_or_404(YearLevel, pk=pk)
    instance.delete()
    message.success(request, "Deleted!")
    return redirect('enrollment:year-level-list')
    
def deleteSubj(request):
    subject =int(request.GET.get('subject'))
    subj = Subjects.objects.get(subject_ID = int(subject))
    subj.delete()
    data = {}
    return JsonResponse(data)


''' ARCHIVE 

#From Create and Update Curriculum
  
def updateCurriculum(request, pk='pk', template='enrollment/curriculum-list-update.html'):
    instance = get_object_or_404(Curriculum, pk=pk)
    context = {'instance': instance}
    return render(request, template, context)

def editCurriculumForm(request, pk='pk', template = 'enrollment/forms-curriculum-edit.html'):
    instance = get_object_or_404(Curriculum, pk=pk)
    last_curriculum = getLatest(Curriculum, 'curriculum_ID')
    data = {'form_is_valid' : False }
    context = {'form': form, 'curriculum':last_curriculum, 'instance': instance}

    forms = updateInstance(request, CurriculumForms, instance)

    if forms.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    return ajaxTable(request,template,context,data)
class sectionDetailFormAutoComp(autocomplete.Select2QuerySetView):
    def query_set(self):
        data = {'form_is_valid' : True }
        section = get_object_or_404(Section, pk=pk)
        section_enrollee = Enrollment.objects.filter(section = section)
        try:
            enrollment = Enrollment.objects.latest('enrollment_ID')
        except:
            enrollment = None
        
        if self.q:
            qs = Enrollment.objects.filter(student__name__icontains=q)
            
        return qs
        
            
        context = {'last_record':enrollment, 'section': section}
        data['html_form'] = render_to_string('enrollment/forms-section-detail-create.html',
            context,
            request=request,
        )
        return JsonResponse(data)


'''