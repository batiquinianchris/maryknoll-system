from django.shortcuts import render, get_object_or_404
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

#Local Functions -- Only for this module#

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
# Custom Functions - Only for this module

#--------------------------------------CURRICULUM------------------------------------------------------
@login_required
def curriculumList(request):
    '''simple error handling: if current year is == year of latest curriculum created, disable the button'''

    try:
        latest_curr = Curriculum.objects.latest('curriculum_year')
    
        if datetime.today().year == latest_curr.get_year():
            disabled = True
    except:
        latest_curr = None
        disabled = False
    #redirect to new page
    return render(request, 'enrollment/curriculum-list.html', context={'disabled':disabled})

def addCurriculumProfile(request):
    #add constraints here
    new_curriculum = Curriculum(curriculum_status='Active')
    new_curriculum.save()
    data = {'form_is_valid' : True }
    return JsonResponse(data)

def openCurriculumSubjectAdd(request, pk='pk'):
    curriculum = Curriculum.objects.get(curriculum_ID=pk)
    return render(request, 'enrollment/curriculum-list-add.html', {'curriculum':curriculum})

def tableCurriculumList(request):
    curriculum_list = Curriculum.objects.all()
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(curriculum_list, 10)
    
    try:
        curriculum = paginator.page(page)
    except PageNotAnInteger:
        curriculum = paginator.page(1)
    except EmptyPage:
        curriculum = paginator.page(paginator.num_pages)
        
    context = {'curriculum_list': curriculum}
    html_form = render_to_string('enrollment/table-curriculum-list.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})

def createCurriculumProfile(request, pk):
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
    data['html_form'] = render_to_string('enrollment/forms-curriculum-subjects-list-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def curriculumDetails(request, pk='pk'):
    curriculum = get_object_or_404(Curriculum, curriculum_ID=pk)
    try:
        last_record = Subjects.objects.filter(curriculum=curriculum).latest('enrollment_ID')
    except:
        last_record = Subjects.objects.filter(curriculum=curriculum)
    return render(request, 'enrollment/curriculum-subjects-list.html', {'curriculum': curriculum, 'record':last_record})
    
def tableCurriculumSubjectList(request, pk='pk'):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    subject_list = Subjects.objects.filter(curriculum = curriculum)
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(subject_list, 4)
    
    try:
        subject = paginator.page(page)
    except PageNotAnInteger:
        subject = paginator.page(1)
    except EmptyPage:
        subject = paginator.page(paginator.num_pages)
        
    context = {'subject_list': subject_list, "curriculum": curriculum}
    html_form = render_to_string('enrollment/table-curriculum-subject-list.html',
        context,
        request = request,
    )
    
    data = {'html_form' : html_form}
    return JsonResponse(data)
    
def updateCurriculum(request, pk='pk'):
    instance = get_object_or_404(Curriculum, pk=pk)
    return render(request, 'enrollment/curriculum-list-update.html', {'instance': instance})
def editCurriculumForm(request, pk='pk'):
    instance = get_object_or_404(Curriculum, pk=pk)
    data = {'form_is_valid' : False }
    try:
        last_curriculum = Curriculum.objects.latest('curriculum_ID')
    except:
        last_curriculum = None
    if request.method == 'POST':
        form = CurriculumForms(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = CurriculumForms(instance = instance)
    context = {'form': form, 'curriculum':last_curriculum, 'instance': instance}
    data['html_form'] = render_to_string('enrollment/forms-curriculum-edit.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def editSubject(request, pk='pk', template = 'enrollment/curriculum-subjects-list-update.html'):
    subject = get_object_or_404(Subjects, pk=pk)
    curriculum_ID = int(request.GET.get('curriculum', None))
    curriculum = Curriculum.objects.get(curriculum_ID=curriculum_ID)
    context = {'subject':subject, 'curriculum':curriculum}
    return render(request, template, context)
    
def form_editSubject(request, pk='pk', template = 'enrollment/forms-curriculum-subjects-list-edit.html'):
    curriculum_ID = request.GET.get('curriculum', None)
    curriculum = Curriculum.objects.get(curriculum_ID=1)
    instance = get_object_or_404(Subjects, subject_ID=pk)
    data = {'form_is_valid' : False }
    

    form = updateInstance(request, SubjectForm, instance)

    if form.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    context = {'form': form, 'curriculum':curriculum, 'instance': instance}
    return ajaxTable(request,template,context,data)
    
#--------------------------------------SECTION--------------------------------------------------------
def sectionList(request):
    return render(request,'enrollment/section-list.html')
    
def addSection(request):
    return render(request, 'enrollment/section-list-add.html')

    
def sectionTable(request):
    section_list = getSectionList(request)
    print section_list
    
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(section_list, 3)
    
    try:
        section = paginator.page(page)
    except PageNotAnInteger:
        section = paginator.page(1)
    except EmptyPage:
        section = paginator.page(paginator.num_pages)
        
    context = {'section_list': section}
    html_form = render_to_string('enrollment/table-section-list.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})
    
def sectionDetails(request, pk='pk'):
    section = get_object_or_404(Section, pk=pk)
    return render(request, 'enrollment/section-details.html', {'section': section})
    
def tableSectionDetail(request, pk='pk'):
    section = get_object_or_404(Section, pk=pk)
    
    section_enrollee_list = Enrollment.objects.filter(section = section)
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(section_enrollee_list, 1)
    
    try:
        section_page = paginator.page(page)
    except PageNotAnInteger:
        sectio_page  = paginator.page(1)
    except EmptyPage:
        section_page = paginator.page(paginator.num_pages)
        
    context = {'section_enrollee_list': section_page}
    html_form = render_to_string('enrollment/table-section-details.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})

def sectionDetailAdd(request, pk='pk'):
    section = get_object_or_404(Section, pk=pk)
    return render(request, 'enrollment/section-details-add.html', {'section': section})

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
                Q(adviser__icontains=search)|
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
            query = Section.objects.filter(adviser__icontains=search)
        else:
            print "wala"
            query = Section.objects.all() 
            
    else:
        return []
    return query
    
def generateSectionForm(request):
    data = {'form_is_valid' : False }
    try:
        last_section = Section.objects.latest('section_ID')
    except:
        last_section = None
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
    print(form.is_valid())
    print(form.errors)
    data['html_form'] = render_to_string('enrollment/forms-section-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def editSection(request, pk='pk',template = 'enrollment/section-list-update.html'):
    instance = get_object_or_404(Section, pk=pk)
    return render(request, template, {'instance': instance})
    
def form_editSection(request, pk='pk', template = 'enrollment/forms-section-edit.html'):
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
def scholarshipList(request):
    return render(request, 'enrollment/scholarship-list.html')

def addScholarshipProfile(request):
    return render(request, 'enrollment/scholarship-list-add.html')
def tableScholarshipList(request):
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
        
    context = {'schoolyear_list': scholarship}
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

def createScholarshipProfile(request):
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
    data['html_form'] = render_to_string('enrollment/forms-scholarship-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def updateScholarship(request, pk='pk'):
    instance = get_object_or_404(Scholarship, pk=pk)
    return render(request, 'enrollment/scholarship-list-update.html', {'instance': instance})


def editScholarshipForm(request, pk='pk'):
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
    data['html_form'] = render_to_string('enrollment/forms-scholarship-edit.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
#--------------------------------------SUBJECT OFFERING------------------------------------------------
@login_required
def subjectOfferingList(request, pk='pk'):
    context = {}
    return render(request, 'enrollment/subject-offering.html', context)
def newSchoolYear(request):
    school_year = School_Year.objects.latest('date_start')
    #redirect page to list

def addSubjectOfferingProfile(request, pk):
    school_year = School_Year.objects.get(id=pk)
    return render(request, 'enrollment/subject-offering-add.html', context= {'school_year':school_year})
def tableSubjectOfferingList(request, pk):
    sy = School_Year.objects.get(id=pk)
    subjectOffering_list = Offering.objects.filter(school_year = sy)
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(subjectOffering_list, 10)
    
    try:
        subjectOffering = paginator.page(page)
    except PageNotAnInteger:
        subjectOffering = paginator.page(1)
    except EmptyPage:
        subjectOffering = paginator.page(paginator.num_pages)
        
    context = {'subjectOffering_list': subjectOffering}
    html_form = render_to_string('enrollment/table-subject-offering.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})

def createSubjectOfferingProfile(request, pk):
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
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SubjectOfferingForms()
    context = {'form': form, 'subjectOffering':last_subjectOffering, 'school_year': curr_sy}
    data['html_form'] = render_to_string('enrollment/forms-subject-offering-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def subjectOfferingDetail(request, pk='pk'):
    subjOffering = get_object_or_404(Student, pk=pk)
    try:
        last_record = Enrollment.objects.filter(subjOffering=subjOffering).latest('enrollment_ID')
    except:
        last_record = Enrollment.objects.filter(subjOffering=subjOffering)
    return render(request, 'enrollment/subject-offering-add.html.html', {'subjOffering': subjOffering, 'record':last_record})
    


def updateSubjectOffering(request, pk='pk'):
    instance = get_object_or_404(Offering, pk=pk)
    return render(request, 'enrollment/subject-offering-update.html', {'instance': instance})


def editSubjectOfferingForm(request, pk='pk'):
    instance = get_object_or_404(Offering, pk=pk)
    data = {'form_is_valid' : False }
    try:
        last_subjectOffering = Offering.objects.latest('subjectOffering_ID')
    except:
        last_subjectOffering = None
    if request.method == 'POST':
        form = SubjectOfferingForms(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = SubjectOfferingForms(instance = instance)
    context = {'form': form, 'subjectOffering':last_subjectOffering, 'instance': instance}
    data['html_form'] = render_to_string('enrollment/forms-subject-offering-edit.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
#--------------------------------------SCHOOL YEAR------------------------------------------------

def schoolYearList(request):
    return render(request,'enrollment/schoolyear-list.html')

def tableSchoolYearList(request):
    schoolyear_list = School_Year.objects.all()
    
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(schoolyear_list, 5)
    
    try:
        school_year = paginator.page(page)
    except PageNotAnInteger:
        school_year = paginator.page(1)
    except EmptyPage:
        school_year = paginator.page(paginator.num_pages)
        
    context = {'schoolyear_list': school_year}
    html_form = render_to_string('enrollment/table-schoolyear-list.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})
    
def createSchoolYear(request):
    return render(request,'enrollment/schoolyear-list-add.html')

def form_createSchoolYear(request):
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
    data['html_form'] = render_to_string('enrollment/forms-schoolyear-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)