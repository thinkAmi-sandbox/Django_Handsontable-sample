from django.db import models

class Header(models.Model):
    update_at = models.DateTimeField('UpdateAt')

class Detail(models.Model):
    header = models.ForeignKey(Header)
    purchase_date = models.DateField('Date')
    name = models.CharField('Name', max_length=255)
    price = models.DecimalField('Price', max_digits=10, decimal_places=0)
