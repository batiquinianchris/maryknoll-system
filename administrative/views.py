from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmployeeForms
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from .models import *
from django.db.models import Q

@login_required
def index(request):
    pass

@login_required
def userList(request):
    return render(request, 'administrative/admin-employee-list.html')

def addEmployeeProfile(request):
    return render(request, 'administrative/admin-employee-list-add.html')

def updateEmployee(request, pk='pk'):
    instance = get_object_or_404(Employee, pk=pk)
    return render(request, 'administrative/admin-employee-list-update.html', {'instance': instance})


    
#AJAX VIEWS --------------------------------------------------------------------
from django.template.loader import render_to_string
from django.http import JsonResponse

def tableEmployeeList(request):
    employee_list = getEmployeeList(request)
    print employee_list
    #Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(employee_list, 5)
    
    try:
        employee = paginator.page(page)
    except PageNotAnInteger:
        employee = paginator.page(1)
    except EmptyPage:
        employee = paginator.page(paginator.num_pages)
        
    context = {'employee_list': employee}
    html_form = render_to_string('administrative/table-employee-list.html',
        context,
        request = request,
    )
    return JsonResponse({'html_form' : html_form})

def createEmployeeProfile(request):
    data = {'form_is_valid' : False }
    try:
        last_employee = Employee.objects.latest('employee_ID')
    except:
        last_employee = None
    if request.method == 'POST':
        form = EmployeeForms(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = EmployeeForms()
    context = {'form': form, 'employee':last_employee}
    data['html_form'] = render_to_string('administrative/forms-employee-create.html',
        context,
        request=request,
    )
    return JsonResponse(data)
    
def updateEmployeeForm(request, pk='pk'):
    instance = get_object_or_404(Employee, pk=pk)
    data = {'form_is_valid' : False }
    try:
        last_employee = Employee.objects.latest('employee_ID')
    except:
        last_employee = None
    if request.method == 'POST':
        form = EmployeeForms(request.POST, instance = instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = EmployeeForms(instance = instance)
    context = {'form': form, 'employee':last_employee, 'instance': instance}
    data['html_form'] = render_to_string('administrative/forms-employee-update.html',
        context,
        request=request,
    )
    return JsonResponse(data)

def getEmployeeList(request):
    search = request.GET.get('search')
    genre = request.GET.get('genre')
    isNum = True
    try:
        int(search)
    except:
        isNum = False
    if(request.GET.get('search')!= "None"):
        if( (genre == "None" or genre == "All Categories") and isNum):
            query = Employee.objects.filter(
                Q(employee_ID__contains=search)|
                Q(first_name__contains=search)|
                Q(last_name__contains=search)|
                Q(work_type__contains=search)|
                Q(emp_type__contains=search)|
                Q(emp_status__contains=search)
            )
        if(genre == "None" or genre == "All categories"):
            query = Employee.objects.filter(
                Q(employee_ID__contains=search)|
                Q(first_name__icontains=search)|
                Q(last_name__icontains=search)|
                Q(work_type__contains=search)|
                Q(emp_type__contains=search)|
                Q(emp_status__contains=search)
            )
        elif(genre == "Full Name"):
            print "name"
            query = Employee.objects.filter(
                Q(first_name__icontains=search)|
                Q(last_name__icontains=search)
            )
        elif(genre == "Employee Type"):
            query = Employee.objects.filter(emp_type=search)
        elif(genre == "Work Type"):
            query = Employee.objects.filter(work_type=search)
            if (search == ""):
                query = Employee.objects.all()
        elif(genre == "Status"):
            query = Employee.objects.filter(emp_status=search)
        else:
            print "wala"
            query = Employee.objects.all()
    else:
        return []
    return query
    