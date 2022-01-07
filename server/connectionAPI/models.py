from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class User(AbstractUser):
    id = models.BigAutoField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=50)
    mtm_database = models.ManyToManyField('Database')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Database(models.Model):
    name = models.CharField(max_length=50)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Table(models.Model):
    id = models.BigAutoField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=50)
    fk_database = models.ForeignKey('Database', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Field(models.Model):
    id = models.BigAutoField(null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=20)
    fk_table = models.ForeignKey('Table', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
