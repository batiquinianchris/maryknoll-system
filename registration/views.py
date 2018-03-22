from django.shortcuts import render, get_object_or_404
from django.views import generic

from django.utils import timezone

from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from .models import *
from .forms import *

from django.template.loader import render_to_string
from django.http import JsonResponse

from django.db import models
from django.http import StreamingHttpResponse
from django.views.generic import View
import csv
from cashier.models import *
from django.http import HttpResponseRedirect
# Global Functions - can be applied anywhere
# EXPORT TO CSV class is at the bottom-most part of this code
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
def getLatest(model, attribute):
    # Get latest record of a model, basing on a certain attribute
    # Returns an instance
    try:
        latest = model.objects.latest(attribute)
    except:
        latest = None
    return latest
def updateInstance(request, modelForm, instance):
    if request.method == 'POST':
        form = modelForm(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
    else:
        form = modelForm(instance = instance)
    return form
# Custom Functions - Only for this module

def getStudentList(request, status = None):
    # Get student list with filters IF there is any, if none, then return all
    # 3/19/2018 - TO DEVELOPED:if there is a second parameter, add status to all search 
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Student.objects.filter(
                Q(student_ID__contains=search)|
                Q(first_name__contains=search)|
                Q(last_name__contains=search)|
                Q(middle_name__contains=search)|
                Q(student_level__contains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Student.objects.filter(
                Q(first_name__contains=search)|
                Q(last_name__contains=search)|
                Q(middle_name__contains=search)|
                Q(student_level__contains=search)
            )
        elif(genre == "Name"):
            query = Student.objects.filter(
                Q(first_name__contains=search)|
                Q(last_name__contains=search)|
                Q(middle_name__contains=search)|
                Q(student_level__contains=search)
            )
        elif(genre == "Student ID" and isNum):
            query = Student.objects.filter(student_ID=search)
        elif(genre == "Year/Level"):
            # This needs debugging. ex. JUNIOR_HIGH == 'j' but input is "Junior High"
            query = Student.objects.filter(student_level=search)
        else:
            print "All Students Returned!"
            query = Student.objects.all() 
            
    else:
        return []
    return query
def verifyActive():
    # Get latest school year, then get the student's latest registration school_year
    # If they are equal, he is in this school year, == He is active 
    student_list = Student.objects.all()
    for curr_student in student_list:
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

# Views

def studentList(request, template='registrar/student-profiles/student-registration-list.html'):
    # Table view - table_StudentList
    return render(request, template)
def table_StudentList(request, template = 'registrar/student-profiles/table-student-list.html'):
    verifyActive()
    
    student_list = getStudentList(request)

    limited_students = paginateThis(request, student_list, 10)

    context = {'student_list': limited_students}

    return ajaxTable(request, template, context)

def table_ActiveList(request, template = 'registrar/student-profiles/table-student-list.html'):
    verifyActive()
    
    student_list = Student.objects.filter(status='a')

    limited_students = paginateThis(request, student_list, 10)

    context = {'student_list': limited_students}
    print context
    return ajaxTable(request, template, context)

def table_InActiveList(request, template = 'registrar/student-profiles/table-student-list.html'):
    verifyActive()
    
    student_list = Student.objects.filter(status='i')
    
    limited_students = paginateThis(request, student_list, 10)

    
    context = {'student_list': limited_students}
    print context
    return ajaxTable(request, template, context)

def table_ScholarList(request, template = 'registrar/student-profiles/table-student-list.html'):
    verifyActive()
    list_of_ids = []
    #Get enrolled students
    student_list = Student.objects.filter(status='a')
    #Get the student's latest registration
    for student in student_list:
        curr_registration = Enrollment.objects.filter(student=student).latest('date_enrolled')
        #Get scholarship list of that enrollment object
        scholar_list = StudentScholar.objects.filter(registration=curr_registration)
        #If this list exists, then the student is a scholar
        if scholar_list:
            list_of_ids.append(student.student_ID)
    #Get list of students from the list of IDs collected
    scholars = Student.objects.filter(student_ID__in=list_of_ids)
    limited_students = paginateThis(request, scholars, 10)

    
    context = {'student_list': limited_students}
    print context
    return ajaxTable(request, template, context)

def addStudent(request, template = 'registrar/student-profiles/student-registration-list-add.html'):
    # Form view - form_addStudent
    return render(request, template)
def form_addStudent(request, template = 'registrar/student-profiles/forms-student-create.html'):
    data = {'form_is_valid' : False }

    if request.method == 'POST':
        form = StudentForms(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = StudentForms()

    last_student = getLatest(Student, 'student_ID')
    context = {'form': form, 'student':last_student}

    return ajaxTable(request, template, context, data)

def updateStudentProfile(request, pk='pk',template = 'registrar/student-profiles/student-registration-list-update.html'):
    instance = get_object_or_404(Student, pk=pk)
    return render(request, template, {'instance': instance})
def form_updateStudentProfile(request, pk='pk', template = 'registrar/student-profiles/forms-student-edit.html'):
    instance = get_object_or_404(Student, pk=pk)
    data = {'form_is_valid' : False }
    last_student = getLatest(Student,'student_ID')

    form = updateInstance(request, StudentForms, instance)

    if form.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    context = {'form': form, 'student':last_student, 'instance': instance}
    return ajaxTable(request,template,context,data)

def studentDetails(request, pk='pk', template='registrar/student-registration/student-profile.html'):
    current_student = get_object_or_404(Student, pk=pk)
    # Get latest record of a model, basing on a certain attribute
    # Returns an instance. This is for models with Foreign Keys
    try:
        last_record = Enrollment.objects.filter(student=current_student).latest('enrollment_ID')
    except:
        last_record = Enrollment.objects.filter(student=current_student)
    print last_record
    return render(request, template, {'student': current_student, 'record':last_record})
def table_studentDetails(request, pk='pk', template = 'registrar/student-registration/table-student-profile.html'):
    student = get_object_or_404(Student, pk=pk)
    enrollment_list = Enrollment.objects.filter(student=student)
    curr_enrollment = getLatest(Enrollment,'enrollment_ID')
    scholarship_list = StudentScholar.objects.filter(registration=curr_enrollment)
    enrollment = paginateThis(request, enrollment_list, 10)
    context = {'enrollment_list': enrollment, 'student':student, 'scholarship': scholarship_list}

    return ajaxTable(request, template, context)

def addEnrollment(request, pk='pk', template='registrar/student-registration/student-profile-add.html'):
    student = Student.objects.get(student_ID = pk)
    return render(request, template, {'student': student})
def form_addEnrollment(request, pk='pk', template = 'registrar/student-registration/forms-registration-create.html'):
    data = {'form_is_valid' : False }

    current_student = get_object_or_404(Student, pk=pk)
    enrollment = getLatest(Enrollment, 'enrollment_ID')

    if request.method == 'POST':
        form = RegistrationForms(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date_enrolled = datetime.date.today()
            post.student = current_student
            post.student_type='n'
            current_student.status="a"
            form.save()
            data['form_is_valid'] = True
        else:
            print form.errors
            data['form_is_valid'] = False
    else:
        form = RegistrationForms()

    # !!! 3/12/2018 -- Jim -- We need to provide two more context variables: Scholarships and Sections
    context = {'form': form, 'student':current_student, 'last_record':enrollment}

    return ajaxTable(request,template,context,data)

def editEnrollment(request, pk='pk', template = 'registrar/student-registration/student-profile-update.html'):
    registration = get_object_or_404(Enrollment, pk=pk)
    student_ID = int(request.GET.get('student', None))
    student = Student.objects.get(student_ID=student_ID)
    context = {'enrollment':registration, 'student':student}
    return render(request, template, context)
    
def form_editEnrollment(request, pk='pk', template = 'registrar/student-registration/forms-registration-edit.html'):
    student_ID = request.GET.get('student', None)
    student = Student.objects.get(student_ID=1)
    instance = get_object_or_404(Enrollment, enrollment_ID=pk)
    data = {'form_is_valid' : False }
    

    form = updateInstance(request, RegistrationForms, instance)

    if form.is_valid():
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False

    context = {'form': form, 'student':student, 'instance': instance}
    return ajaxTable(request,template,context,data)
def generateStudentCode(student):
    pass


def table_studentScholar(request,pk='pk',template='registrar/student-registration/scholarships-list.html'):
    registration = Enrollment.objects.get(enrollment_ID=pk)
    scholarship_list = StudentScholar.objects.filter(registration=registration)
    curr_sy = School_Year.objects.latest('pk')
    active = registration.school_year == curr_sy
    context = {'scholarship_list':scholarship_list, 'student':registration.student, 'active':active}
    return ajaxTable(request,template,context)


def deleteScholar(request):
    schol_id =int(request.GET.get('scholar'))
    scholar = StudentScholar.objects.get(id = schol_id)
    scholar.delete()
    data = {}
    return JsonResponse(data)


def StudentScholarFormView(request, pk='pk',template = "registrar/student-registration/student-scholarship-add.html" ):
    print pk
    regist = Enrollment.objects.get(enrollment_ID=pk)
    
    if request.method == 'POST':
        form = StudentScholarForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.registration = regist
            form.save()
            return HttpResponseRedirect(reverse('student-details',kwargs={'pk':regist.student.student_ID}))
        else:
            print form.errors
    else:
        form = StudentScholarForm()
    
    context = {'form':form, 'student':regist.student}

    return render(request, template, context)

def tableTransactionLogs(request,pk='pk',template="registrar/student-registration/table-transaction-logs.html"):
    registration = Enrollment.objects.get(enrollment_ID=pk)

    transaction_list = EnrollmentTransactionsMade.objects.filter(student=registration)
    
    context = {'transaction_list_enrollment': transaction_list, 'registration':registration}
    return ajaxTable(request,template,context)

        
def subjectsView(request, pk='pk', template='registrar/student-registration/table-student-subjects.html'):
    section = Section.objects.get(pk=pk)
    offerings_list = Offering.objects.filter(section=section)
    context = {'offering_list':offerings_list, 'section':section}
    return ajaxTable(request,template,context)