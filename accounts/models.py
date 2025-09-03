from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Partner', 'Partner'),
        ('Associate', 'Associate'),
        ('Secretary', 'Secretary'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username



