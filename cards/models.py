from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class CardList(models.Model):
    username = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    bank = models.CharField(max_length = 100)
    card = models.BigIntegerField(validators = [MinLengthValidator(12)])
    pvtkey = models.CharField(null=True, max_length = 100)
    binary = models.CharField(null=True, max_length = 100)
