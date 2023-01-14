from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CustomAttrsMixin(models.Model):
    """ Добавляем каждой модели некий кастомный атрибут в виде JSONField """
    custom_attrs = models.JSONField(null=True)

    class Meta:
        abstract = True


class Portfolio(CustomAttrsMixin, models.Model):
    name = models.CharField(max_length=32)
    notes = models.TextField()
    strategy = models.TextField()


class Currency(CustomAttrsMixin, models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=8)


class Instrument(CustomAttrsMixin, models.Model):
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    isin = models.CharField(max_length=12)
    description = models.TextField()
    maturity_date = models.DateField()
    accrual_size = models.DecimalField(max_digits=10, decimal_places=2)
    accrual_date = models.DateField()


class Account(CustomAttrsMixin, models.Model):
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=8)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Transaction(CustomAttrsMixin, models.Model):
    transaction_date = models.DateField()
    type = models.CharField(max_length=8)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE)
    instrument = models.ForeignKey(to=Instrument, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(to=Portfolio, on_delete=models.CASCADE)
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    notes = models.TextField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
