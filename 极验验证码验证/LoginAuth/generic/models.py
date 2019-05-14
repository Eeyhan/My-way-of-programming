from django.db import models


# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户姓名")
    pwd = models.CharField(max_length=32, verbose_name="密文密码")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'db_Acount'
        db_table = verbose_name_plural
