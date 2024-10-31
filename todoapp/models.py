from django.db import models

# Create your models here.
class Todo(models.Model):
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Numero = models.CharField(max_length=100)
    Date_vm = models.DateTimeField(null=True , blank=True)
    Date_fts = models.DateField(null=True , blank=True)