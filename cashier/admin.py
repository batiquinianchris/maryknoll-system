from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(EnrollmentBreakdown)
admin.site.register(EnrollmentTransactionsMade)
admin.site.register(EnrollmentORDetails)
admin.site.register(OthersORDetails)
admin.site.register(OthersTransactionsMade)