from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(50)
    mtm_database = models.ManyToManyField('Database')


class Database(models.Model):
    name = models.CharField(50)
    type = models.CharField(20)

class Tables(models.Model):
    name = models.CharField(50)
    fk_database = models.ForeignKey(null=True, on_delete=models.CASCADE)

class Field(models.Model):
    name = models.CharField(20)
    fk_table = models.ForeignKey(null=True, on_delete=models.CASCADE)




