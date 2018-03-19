from django.conf.urls import url, include

from . import views
#Fees and accounts
urlpatterns = [
        url(r'^fees-and-accounts$', views.openFeeAccount, name = 'fees-and-accounts'),
        url(r'^fees-and-accounts/add$', views.openFeeAccountAdd, name = 'fees-and-accounts-add'),
        url(r'^fees-and-accounts/edit/(?P<pk>\d+)$', views.openFeeAccountEdit, name = 'fees-and-accounts-edit'),
        url(r'^fees-and-accounts/table$', views.tableFeeAccount, name = 'table-fees-and-accounts'),
        url(r'^fees-and-accounts/add/form$', views.formFeeAccountAdd, name = 'form-fees-and-accounts-add'),
        url(r'^fees-and-accounts/edit/form/edit/(?P<pk>\d+)$', views.formFeeAccountEdit, name = 'form-fees-and-accounts-edit'),
    ]

#Transactions
urlpatterns += [
    url(r'^transaction/(?P<pk>\d+)$', views.transactionView , name='transaction'),
    url(r'^transaction/payment-summary/(?P<pk>\d+)$', views.summaryView , name='payment-summary'),
]