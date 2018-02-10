from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from datetime import datetime

# Create your models here.
''' TAIL ENTITIES '''
#Equivalent to student registration form (Part 1)
ACTIVE = 'a'
INACTIVE = 'i'
MALE = 'm'
FEMALE = 'f'
OTHERS = 'o'
GRADE = 'g'
JUNIOR = 'j'
SENIOR = 's'
class Student(models.Model):
    student_ID = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    #student level
    LEVEL_CHOICES = (
        (GRADE, 'Grade School'),
        (JUNIOR, 'Junior High'),
        (SENIOR, 'Senior High'),
        (OTHERS, 'Others')
    )
    student_level = models.CharField(max_length=1,
        choices=LEVEL_CHOICES,
        blank=False,
        default=OTHERS
        )
    #student gender
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1,
        choices=GENDER_CHOICES,
        blank=False,
        default=OTHERS
        )
    #student status
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )
    status = models.CharField(max_length=1,
        choices=STATUS_CHOICES,
        blank=False,
        default=INACTIVE
        )
    #other attributes
    birthplace = models.CharField(max_length=200)
    birthdate = models.DateField(auto_now=False)
    home_addr = models.CharField(max_length=200)
    postal_addr = models.CharField(max_length=200)
    m_firstname = models.CharField(max_length=200)
    m_middlename = models.CharField(max_length=200)
    m_lastname = models.CharField(max_length=200)
    m_occcupation = models.CharField(max_length=200)
    f_firstname = models.CharField(max_length=200)
    f_middlename = models.CharField(max_length=200)
    f_lastname = models.CharField(max_length=200)
    f_occupation = models.CharField(max_length=200)
    guardian = models.CharField(max_length=200)
    guardian_addr = models.CharField(max_length=200)
    last_school = models.CharField(max_length=200)
    '''Model Configuration'''
    class Meta:
        ordering = ["student_ID"]
        #allow only people with permissions
        #permissions = ((),)
    def get_absolute_url(self):
        """**important in detail-view
        Returns the url to access a particular instance.
        """
        return reverse('student-details', args=[str(self.student_ID)])
    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s, %s - %s' % (self.student_ID, self.first_name, self.status)

#Equivalent to student registration form (part2)

PAID = 'p'
INCOMPLETE = 'i'
NO_PAY = 'n'
DROPPED = 'd'

class Enrollment(models.Model):
    enrollment_ID = models.AutoField(primary_key=True)
    curriculum = models.ForeignKey('enrollment.Curriculum', on_delete=models.CASCADE, default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=0)
    scholarship = models.ForeignKey('enrollment.Scholarship', on_delete=models.CASCADE, default=0)
    date_enrolled = models.DateField(auto_now_add=True)
    '''Type enum '''
    TYPE_CHOICES = (
        (PAID,'Paid'),
        (INCOMPLETE,'Incomplete'),
        (NO_PAY,'Payment Not Made'),
        (DROPPED, 'Dropped out'),
        )
    
    school_year = models.ForeignKey('enrollment.School_Year', on_delete=models.SET_NULL, null=True)
    student_type = models.CharField(max_length=1,choices=TYPE_CHOICES,blank=False,default=NO_PAY)
    
    
    class Meta:
        verbose_name = "Enrollment"
        
    def __str__(self):
        return "%s enrolled under %s" % (self.student, self.curriculum)
    #For detailed view
    def get_absolute_url(self):
        return reverse('enrollment-table', args=[str(self.enrollment_ID)])


class Drop(models.Model):
    drop_ID = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    drop_date = models.DateField(auto_now_add=True)
    curriculum = models.ForeignKey('enrollment.Curriculum', on_delete=models.CASCADE, default=0)
    title = models.CharField(max_length=200)
    reason = models.CharField(max_length=500)
    status = models.CharField(max_length=2)
    approved_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Drop"
    def __str__(self):
        return "%s - %s" %(self.student, self.title)
        
    def get_absolute_url(self):
        return reverse('!!!!!', args=[str(self.drop_ID)])

	