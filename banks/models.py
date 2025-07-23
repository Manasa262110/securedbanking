from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class BankList(models.Model):
    name = models.CharField(max_length = 100)
    btype = models.CharField(max_length = 100)
    hq = models.CharField(max_length = 100)
    estd = models.PositiveIntegerField(validators=[RegexValidator(regex='^.{4}$', message='Length has to be 4', code='nomatch')])
