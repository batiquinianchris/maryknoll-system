from __future__ import unicode_literals
from django.db.models import Sum
from django.db import models

#SIGNALS = TRIGGERS
from django.db.models.signals import post_save
# Create your models here.
class EnrollmentBreakdown(models.Model):
    """Model definition for EnrollmentBreakdown."""
    payable_name = models.CharField(max_length=50)
    fee_amount = models.FloatField()
    year_level = models.ForeignKey(
        'enrollment.YearLevel', on_delete=models.CASCADE, null=True,blank=True)
    
    class Meta:
        """Meta definition for EnrollmentBreakdown."""

        verbose_name = 'EnrollmentBreakdown'
        verbose_name_plural = 'EnrollmentBreakdowns'

    def __str__(self):
        """Unicode representation of EnrollmentBreakdown."""
        return "%s" (self.payable_name)


class EnrollmentTransactionsMade(models.Model):
    student = models.ForeignKey(
        'registration.Enrollment', on_delete=models.CASCADE)
    
    date_paid = models.DateField()
    ORnum = models.CharField(max_length=100,blank=True,null=True)
    method_CHOICES = (
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Promissory', 'Others'),
        ('Others', 'Others'),
    )
    payment_method = models.CharField(max_length=50,
    choices=method_CHOICES,)
    class Meta:
        """Meta definition for EnrollmentTransactionsMade."""

        verbose_name = 'EnrollmentTransactionsMade'
        verbose_name_plural = 'EnrollmentTransactionsMades'

    def get_total_sum(self):
        #Get list of fees for a grade level
        fees_list = EnrollmentORDetails.objects.filter(ORnumber=self)
        #Get total amount of fees
        amount = fees_list.aggregate(Sum('money_given'))
        # amount['money_given__sum']
        return amount['money_given__sum']

    def __str__(self):
        """Unicode representation of EnrollmentTransactionsMade."""
        return str(self.ORnum)


class EnrollmentORDetails(models.Model):
    """Model definition for OR_Details."""
    ORnumber = models.ForeignKey(
        EnrollmentTransactionsMade, on_delete=models.CASCADE)
    money_given = models.FloatField()
    
    name_CHOICES = (
        ('ENROLLMENT', 'Enrollment Fee'),
        ('TUITION', 'Tuition Fee'),
    )
    particular_name = models.CharField(max_length=50,
        choices=name_CHOICES,
        blank=False,
        )
    type_CHOICES = (
        ('FULL', 'Full Payment'),
        ('PART', 'Partial Payment'),
    )
    payment_type = models.CharField(max_length=50,
        choices=type_CHOICES,
        null=True,
        blank=True,
        )
    
    month_CHOICES = (
        ('JAN', 'January'),
        ('FEB', 'Febuary'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    )
    month = models.CharField(max_length=50,
        choices=month_CHOICES,
        null=True, blank=True)
    #remarks
    class Meta:
        """Meta definition for OR_Details."""

        verbose_name = 'OR_Details'
        verbose_name_plural = 'OR_Detailss'

    def __str__(self):
        """Unicode representation of OR_Details."""
        return "%s - %s" %(self.particular_name, str(self.money_given))


class OthersTransactionsMade(models.Model):
    """Model definition for OthersTransactionsMade."""

    student = models.ForeignKey(
        'registration.Enrollment', on_delete=models.CASCADE)
    date_paid = models.DateField()
    ORnum = models.IntegerField()

    class Meta:
        """Meta definition for OthersTransactionsMade."""

        verbose_name = 'OthersTransactionsMade'
        verbose_name_plural = 'OthersTransactionsMades'

    def __str__(self):
        """Unicode representation of OthersTransactionsMade."""
        pass


class OthersORDetails(models.Model):
    """Model definition for OthersORDetails."""

    ORnumber = models.ForeignKey(
        'OthersTransactionsMade', on_delete=models.CASCADE)
    name_of_item = models.CharField(max_length=50)
    money_given = models.FloatField()

    class Meta:
        """Meta definition for OthersORDetails."""

        verbose_name = 'OthersORDetails'
        verbose_name_plural = 'OthersORDetailss'

    def __str__(self):
        """Unicode representation of OthersORDetails."""
        pass
