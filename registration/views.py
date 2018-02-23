from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from enrollment.models import *
from .models import *
from .forms import StudentForms, RegistrationForms

#STATIC VIEWS ------------------------------------------------------------------
@login_required
def index(request):
    pass
    #return render(request,'/registration/index.html',)

@login_required
def registrationList(request):
    return render(request, 'registrar/student-registration-list.html')

def addStudentProfile(request):
    return render(request, 'registrar/student-registration-list-add.html')

@login_required
def studentDetails(request, pk='pk'):
    student = get_object_or_404(Student, pk=pk)
    try:
        last_record = Enrollment.objects.filter(student=student).latest('enrollment_ID')
    except:
        last_record = Enrollment.objects.filter(student=student)
    return render(request, 'registrar/student-profile.html', {'student': student, 'record':last_record})
    
def addEnrollment(request, pk = 'pk'):
    student = Student.objects.get(student_ID = pk)
    return render(request, 'registrar/student-profile-add.html', {'student': student})
#AJAX VIEWS --------------------------------------------------------------------
from django.template.loader import render_to_string
from django.http import JsonResponse

def searchStudent(request):
    search = request.GET.get('search', None)
    data = {
        'is_taken': Student.objects.filter(first_name__contains=search).exists()
    }
    return JsonResponse(data)

def tableStudentList(request):
    verifyActive()
    student_list = Student.objects.all()
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(student_list, 10)
    
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
        
    context = {'student_list': students}
    html_form = render_to_string('registrar/table-student-list.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})

def createStudentProfile(request):
    data = {'form_is_valid' : False }
    try:
        last_student = Student.objects.latest('student_ID')
    except:
        last_student = None
    if request.method == 'POST':
        form = StudentForms(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = StudentForms()
    context = {'form': form, 'student':last_student}
    data['html_form'] = render_to_string('registrar/forms-student-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def tableEnrollmentList(request, pk='pk'):
    student = get_object_or_404(Student, pk=pk)
    
    enrollment_list = Enrollment.objects.filter(student = student)
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(enrollment_list, 4)
    
    try:
        enrollments = paginator.page(page)
    except PageNotAnInteger:
        enrollments = paginator.page(1)
    except EmptyPage:
        enrollments = paginator.page(paginator.num_pages)
        
    context = {'enrollment_list': enrollments}
    html_form = render_to_string('registrar/table-student-profile.html',
        context,
        request = request,
    )
    
    data = {'html_form' : html_form}
    return JsonResponse(data)

def createEnrollment(request, pk='pk'):
    data = {'form_is_valid' : False }
    current_student = get_object_or_404(Student, pk=pk)
    try:
        enrollment = Enrollment.objects.latest('enrollment_ID')
    except:
        enrollment = None
    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        form.date_enrolled = datetime.now()
        form.student = Student.objects.get(student_ID = pk)
        if form.is_valid():
            post = form.save(commit=False)
            post.student_type='n'
            current_student.status="a"
            form.save()
            data['form_is_valid'] = True
        else:
            print form.errors
            data['form_is_valid'] = False
    else:
        form = RegistrationForms()
    context = {'form': form, 'student':current_student, 'last_record':enrollment}
    data['html_form'] = render_to_string('registrar/forms-registration-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def verifyActive():
    student_list = Student.objects.all()
    for curr_student in student_list:
        print(curr_student)
        try:
            last_record = Enrollment.objects.get(student=curr_student.student_ID)
        except:
            last_record = None
        try:
            curr_schoolyear = School_Year.objects.latest('year_name')
        except:
            curr_schoolyear = None
        if ((curr_schoolyear == None) or (last_record == None)):
            break
        elif (curr_schoolyear == last_record.school_year):
            curr_student.status = "a"
            curr_student.save()
            
        