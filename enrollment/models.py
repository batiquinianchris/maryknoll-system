from __future__ import unicode_literals

from django.db import models
#import registration
#import administrative

# Create your models here.

ACTIVE = 'a'
ON_LEAVE = 'o'
INACTIVE = 'i'

ESC = 'e'
OTHERS = 't'

class TeacherDetails(models.Model):
    teacher_ID = models.AutoField(primary_key=True)
    employee_name = models.ForeignKey('administrative.Employee', on_delete= models.SET_NULL, null = True)
    units = models.IntegerField()
    class Meta:
        verbose_name = "Details of Teacher"
        
    def __str__(self):
        return str(self.employee_name)



class School_Year(models.Model):
	year_name = models.CharField(max_length=200)
	date_start = models.DateField(auto_now = True)
	date_end = models.DateField(null=True, blank=True)
	
	class Meta:
	    verbose_name = "School Year"
	    
	def __str__(self):
	    return self.year_name

class YearLevel(models.Model):
    grade_level = models.CharField(max_length=200)
    
    def __str__(self):
        return self.grade_level

class Scholarship(models.Model):
	scholarship_name = models.CharField(max_length=200)
	school_year = models.ForeignKey(School_Year, on_delete=models.CASCADE, default=0)
	SCHOLARSHIP_CHOICES = (
        (ESC, 'ESC'),
        (OTHERS, 'Others'),
    )
	scholarship_type = models.CharField(max_length=1,
        choices=SCHOLARSHIP_CHOICES,
        blank=False,
        default=OTHERS
        )
	
	class Meta:
	    verbose_name = "Scholarship"
	    
	def __str__(self):
	    return "%s for %s" % (self.scholarship_name, self.school_year)
	''' SCHOLARSHIP must only contain scholarship details, not the price/amount it discounts. The money part will be handled in the cashier module'''

class Curriculum(models.Model):
    curriculum_ID = models.AutoField(primary_key=True)
    year_level = models.ForeignKey(YearLevel, on_delete=models.CASCADE)
    school_year = models.ForeignKey(School_Year, on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name = "Curriculum"
        
    def __str__(self):
        return "%s - %s" % (self.year_level, self.school_year)

class Subjects(models.Model):
    subject_ID = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=200)
    subject_description = models.CharField(max_length=200)
    #Subject status
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (ON_LEAVE, 'On Leave'),
        (INACTIVE, 'Inactive'),
    )
    subject_status = models.CharField(max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        default=INACTIVE
        )
        
    curriculum = models.ForeignKey(Curriculum, on_delete = models.SET_NULL, null = True)
    
    class Meta:
        verbose_name = "Subject"
        
    def __str__(self):
        return self.subject_name

class Offering(models.Model):
	offering_ID = models.AutoField(primary_key=True)
	subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=0)
	teacher = models.ForeignKey(TeacherDetails, on_delete=models.CASCADE, default=0)
	school_year = models.ForeignKey(School_Year, on_delete=models.CASCADE, default=0)
	
	class Meta:
	    verbose_name = "Offered Subject"
	def __str__(self):
	    return "%s - - - %s" % (self.subject, self.subject.subject_description)
	    
''' SCHEDULING WILL BE DEVELOPED IN A DIFFERENT APP '''
	
 
class Section(models.Model):
    section_ID = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=50)
    section_capacity = models.IntegerField()
    adviser = models.ForeignKey(TeacherDetails, on_delete = models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete = models.SET_NULL, null = True)
    room = models.CharField(max_length=50)
    #Section status
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    section_status = models.CharField(max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        default=INACTIVE
        )
        
    class Meta:
        verbose_name = "Section"
    def __str__(self):
        return "%s - %s" % (self.year_level,self.section_name)
       
class Section_Enrollee(models.Model):
    enrollee = models.ForeignKey('registration.Enrollment', on_delete=models.CASCADE, default=0)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    section_status = models.CharField(max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        default=INACTIVE
        )
    class Meta:
	    verbose_name = "Enrollees in Sections"
    def __str__(self):
        return "%s enrolled in %s" % (self.enrollee, self.section)
class Section_Offerings(models.Model):
	sectionDetails_ID = models.AutoField(primary_key=True)
	section_ID = models.ForeignKey(Section, on_delete=models.CASCADE, default=0)
	offering_ID = models.ForeignKey(Offering, on_delete=models.CASCADE, default=0)
	
	class Meta:
	    verbose_name = "Section Detail"
	    
	def __str__(self):
	    return "%s - %s" % (self.section_ID, self.offering_ID)
    
class SHS_Subjects(models.Model):
    s_subjectName  = models.CharField(max_length=200)
    s_subjectDesc = models.CharField(max_length=200)
    s_desc = models.CharField(max_length=100)
    s_curriculum = models.ForeignKey(Curriculum, on_delete = models.CASCADE)
    #SHS track status
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    s_status = models.CharField(max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        default=INACTIVE
        )
        
    class Meta:
        verbose_name = "Senior High Subject"
        
    def __str__(self):
        return self.s_subjectName
        
        
class SHS_Offering(models.Model):
    offering_ID = models.AutoField(primary_key=True)
    subject = models.ForeignKey(SHS_Subjects, on_delete=models.CASCADE, default=0)
    teacher = models.ForeignKey(TeacherDetails, on_delete=models.CASCADE, default=0)
    school_year = models.ForeignKey(School_Year, on_delete=models.CASCADE, default=0)
	
    class Meta:
        verbose_name = "Offered Subjects for SHS"
    def __str__(self):
        return "%s - - - %s" % (self.subject, self.offering_ID)
