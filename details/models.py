from django.db import models

# Create your models here.

class ContactDetails(models.Model):
    phone = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    address = models.TextField()
