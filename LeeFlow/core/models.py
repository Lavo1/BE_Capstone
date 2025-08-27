from django.db import models
from accounts.models import CustomUser

class Case(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('On Hold', 'On Hold'),
    )
    case_title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='cases')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    deadline = models.DateField()

    def __str__(self):
        return f"{self.case_title} - {self.client_name}"

class TimeEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='time_entries')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='time_entries')
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    date_logged = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.case.case_title} - {self.hours_worked}h"

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Overdue', 'Overdue'),
    )
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='invoices')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Unpaid')
    date_issued = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"Invoice {self.id} - {self.case.case_title} - {self.total_amount}"
