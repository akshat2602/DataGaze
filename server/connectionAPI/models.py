from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=50)
    mtm_database = models.ManyToManyField('Database')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Database(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tables(models.Model):
    name = models.CharField(max_length=50)
    fk_database = models.ForeignKey('Database', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Field(models.Model):
    name = models.CharField(max_length=20)
    fk_table = models.ForeignKey('Tables', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




