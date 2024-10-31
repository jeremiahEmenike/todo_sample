from .models import Todo
from django import forms

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = '__all__'

        label = {
        "Nom" : "Nom",
        "Prenom" : "Prenom",
        "Numero" : "Numero",
        "Date_vm" : "Date_vm",
        "Date_fts" : "Date_fts",
        }

        widgets ={
        "Nom" : forms.TextInput(attrs={"placeholder":""}),
        "Prenom" : forms.TextInput(attrs={"placeholder":"Prénom usuel"}), 
        "Numero" : forms.TextInput(attrs={"placeholder":"Avec l'indicatif"}),
        "Date_vm" : forms.DateInput(
                        attrs={
                            'class':'form-control',
                            'type':'datetime-local'
                            }),
                            
        "Date_fts" : forms.DateInput(
                        attrs={
                            'class':'form-control',
                            'type':'date'
                            }),
                            
        }