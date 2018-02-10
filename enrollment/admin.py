from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(School_Year)
admin.site.register(Scholarship)
admin.site.register(Curriculum)
admin.site.register(Subjects)
admin.site.register(Offering)
admin.site.register(Section)
admin.site.register(Section_Offerings)
admin.site.register(Section_Enrollee)
admin.site.register(TeacherDetails)
admin.site.register(SHS_Subjects)
admin.site.register(YearLevel)