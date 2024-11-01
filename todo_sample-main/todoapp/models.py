from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import send_appointment_sms
# Create your models here.
class Todo(models.Model):
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Numero = models.CharField(max_length=100)
    Date_vm = models.DateTimeField(null=True , blank=True)
    Date_fts = models.DateField(null=True , blank=True)