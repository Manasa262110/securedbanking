from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
	pic = models.ImageField(upload_to='img/', null=True)
	gender = models.CharField(null=True, max_length=30)
	dob = models.DateField(null=True, )
	bank = models.CharField(null=True, max_length=100)
	mobile = models.CharField(null=True, max_length=10)
	branch = models.CharField(null=True, max_length=100)
	balance = models.DecimalField(default=0.00, max_digits=10,decimal_places=2)
