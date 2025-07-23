from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Transactions(models.Model):
    to_account = models.CharField(max_length = 100)
    from_account = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    card = models.CharField(max_length=255)
    bank = models.CharField(max_length = 100)
    time = models.DateTimeField(auto_now_add=True)
    txntype = models.CharField(max_length = 100)
    amount = models.DecimalField(default=0.00, max_digits = 10, decimal_places = 2)
    txnstatus = models.BooleanField(default=False)
