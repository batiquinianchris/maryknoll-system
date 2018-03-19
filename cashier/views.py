from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.db.models import Sum
# FOR AJAX IMPORTS
from django.template.loader import render_to_string
from django.http import JsonResponse

# IMPORTED MODELS
from .models import *
from registration.models import *
from enrollment.models import *
# Global Functions


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


def ajaxTable(request, template, context, data=None):
    # For templates that needs ajax
    html_form = render_to_string(template,
                                 context,
                                 request=request,
                                 )
    if data:
        data['html_form'] = html_form
    else:
        data = {'html_form': html_form}
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
        form = modelForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            instance.save()
    else:
        form = modelForm(instance=instance)
    return form

# LOCAL FUNCTIONS

def getTotalGradeLevelPayment(grade_level_instance):
    #Get list of fees for a grade level
    fees_list = EnrollmentBreakdown.objects.filter(year_level=grade_level_instance)
    #Get total amount of fees
    amount = fees_list.aggregate(Sum('fee_amount'))
    
    return amount['fee_amount__sum']

def getTotalpayment(registration):
    #get list of transactions made by a registration
    transacts_list = EnrollmentTransactionsMade.objects.filter(student=registration)
    #get total of all transactions
    amount = float(0)
    for transaction in transacts_list:
        transaction_list = EnrollmentORDetails.objects.filter(ORnumber=transaction)
        transact_total = transaction_list.aggregate(Sum('money_given'))
        amount += transact_total['money_given__sum']
    return amount
def getTotalDeductions(registration):
    scholar_list = StudentScholar.objects.filter(registration=registration)
    amount = float(0)
    for scholarship in scholar_list:
        amount += scholarship.scholar.fee_amount
    return amount
# Views
def index(request):
    return render(request, 'index.html')

# FEES AND ACCOUNTS || PARTICULARS #


def openFeeAccount(request, template='cashier/fees-and-accounts/cashier-fees-and-accounts.html'):
    return render(request, template)


def tableFeeAccount(request, template='cashier/fees-and-accounts/table-cashier-fees-and-accounts.html'):
    particulars_list = EnrollmentBreakdown.objects.all()
    # Pagination
    page = request.GET.get('page', 1)
    particulars = paginateThis(request, particulars_list, 10)
    context = {'particulars': particulars}

    return ajaxTable(request, template, context)


def openFeeAccountAdd(request, template='cashier/fees-and-accounts/cashier-fees-and-accounts-add.html'):
    return render(request, template)


def formFeeAccountAdd(request, template='cashier/fees-and-accounts/forms-cashier-fees-and-accounts-add.html'):
    data = {'form_is_valid': False}
    if request.method == 'POST':
        form = EnrollmentBreakdownForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.particular_details = "Auto-generated"

            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = EnrollmentBreakdownForm()
    context = {'form': form}
    return ajaxTable(request, template, context, data)


def openFeeAccountEdit(request, pk='pk', template='cashier/fees-and-accounts/cashier-fees-and-accounts-edit.html'):
    particular = EnrollmentBreakdown.objects.get(pk=pk)
    context = {'particular': particular}
    return render(request, template, context)


def formFeeAccountEdit(request, pk='pk', template='cashier/fees-and-accounts/forms-cashier-fees-and-accounts-edit.html'):
    particular = EnrollmentBreakdown.objects.get(pk=pk)
    data = {'form_is_valid': False}
    if request.method == 'POST':
        form = EnrollmentBreakdownForm(request.POST, instance=particular)
        if form.is_valid():
            particular = form.save()
            particular.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = EnrollmentBreakdownForm(instance=particular)
    context = {'form': form, 'particular': particular}
    return ajaxTable(request, template, context, data)

# END PARTICULARS #
# ACCOUNTS #


# END ACCOUNTS #
# TRANSACTIONS #
def transactionView(request,pk='pk',template='cashier/transactions/payment-transaction.html'):
    registration = Enrollment.objects.get(enrollment_ID=pk)
    context = {'registration':registration}
    return render(request,template,context)

def summaryView(request, pk='pk',template="cashier/transactions/payment-summary.html"):
    
    registration = Enrollment.objects.get(enrollment_ID = pk)
    offering = Offering.objects.latest('year_level')
    studentGradeLevelAccount = getTotalGradeLevelPayment(offering.year_level)
    if studentGradeLevelAccount == None:
        studentGradeLevelAccount = float(0)
    totalPaymentOfStudent = getTotalpayment(registration)
    if totalPaymentOfStudent == None:
        totalPaymentOfStudent = float(0)
    account_balance  = studentGradeLevelAccount - totalPaymentOfStudent
    
    deductions = getTotalDeductions(registration)
    
    #print account_balance
    context = {'student': registration.student,
        'account_balance':account_balance, 
        'amount_paid': totalPaymentOfStudent,
        'scholarship_deductions': deductions,    
    }

    return ajaxTable(request,template,context)

# END DAILY CASH #
