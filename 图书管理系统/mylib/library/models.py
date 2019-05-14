from django.db import models

# Create your models here.

class libdata(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    pub_date = models.DateField()
    athor = models.CharField(max_length=10)
    publish = models.CharField(max_length=30)
