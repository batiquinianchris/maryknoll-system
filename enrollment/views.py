<<<<<<< HEAD
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CurriculumForms
=======
from django.shortcuts import render
from .models import *
from .forms import *
from django.template.loader import render_to_string
from django.http import JsonResponse
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import *

@login_required
def index(request):
    pass
#--------------------------------------CURRICULUM------------------------------------------------------
@login_required
def curriculumList(request):
    return render(request, 'enrollment/curriculum-list.html')

<<<<<<< HEAD
def addCurriculumProfile(request):
    return render(request, 'enrollment/curriculum-list-add.html')
#--------------------------------------SCHOLARSHIP----------------------------------------------------
@login_required
def scholarshipList(request):
    return render(request, 'enrollment/scholarship-list.html')
    
#AJAX VIEWS --------------------------------------------------------------------
from django.template.loader import render_to_string
from django.http import JsonResponse
#--------------------------------------CURRICULUM------------------------------------------------------
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

def createCurriculumProfile(request):
    data = {'form_is_valid' : False }
    try:
        last_curriculum = Curriculum.objects.latest('curriculum_ID')
    except:
        last_curriculum = None
    if request.method == 'POST':
        form = CurriculumForms(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = CurriculumForms()
    context = {'form': form, 'curriculum':last_curriculum}
    data['html_form'] = render_to_string('enrollment/forms-curriculum-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
#--------------------------------------SECTION--------------------------------------------------------
=======
#STATIC VIEWS ------------------------------------------------------------------
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80
def sectionList(request):
    section_list = Section.objects.all()
    context = {
        'section_list' : section_list
    }
    return render(request,'enrollment/section-list.html', context)
<<<<<<< HEAD
#--------------------------------------SCHOLARSHIP----------------------------------------------------
def tableScholarshipList(request):
    scholarship_list = Scholarship.objects.all()
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(scholarship_list, 10)
    
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

'''def createScholarshipProfile(request):
    data = {'form_is_valid' : False }
    try:
        last_scholarship = Scholarship.objects.latest('scholarship_ID')
    except:
        last_scholarship = None
    if request.method == 'POST':
        form = ScholarshipForms(request.POST)
=======
    
def addSection(request):
    return render(request, 'enrollment/section-details-add.html')
    
def sectionDetails(request, pk='pk'):
    section = get_object_or_404(Section, pk=pk)
    
    return render(request, 'enrollment/student-details.html', {'section': section})
    
#AJAX VIEWS --------------------------------------------------------------------

def generateSectionForm(request):
    data = {'form_is_valid' : False }
    try:
        last_section = Section.objects.latest('section_ID')
    except:
        last_section = None
    if request.method == 'POST':
        form = SectionForms(request.POST)
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
<<<<<<< HEAD
        form = ScholarshipForms()
    context = {'form': form, 'scholarship':last_scholarship}
    data['html_form'] = render_to_string('enrollment/forms-scholarship-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)'''
=======
        form = SectionForms()
    context = {'form': form, 'section':last_section}
    print form
    data['html_form'] = render_to_string('enrollment/forms-section-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
>>>>>>> f63eab60e0856a440db3511d6c9df8cdb0354e80
