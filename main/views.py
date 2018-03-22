from django.shortcuts import render
from django.views import generic
from enrollment.models import School_Year
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def dashboard(request, template='dashboard.html'):
    return render(request,template,)
    
@login_required
def settings(request,template = 'settings.html'):
    try:
        latest_sy = School_Year.objects.latest('date_start')
    except:
        latest_sy = None
    return render(request,template, context={'school_year':latest_sy})

@login_required
def reports(request, template="administrative/reports/admin-reports.html"):
    context = {}
    return render(request, template, context)