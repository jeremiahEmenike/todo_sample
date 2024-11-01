from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import TodoForm
from .models import Todo
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
import mysql.connector
from django.conf import settings
from datetime import datetime


# Create your views here.   

@login_required
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is None:
            context ={"error": "Invalid username or password"}
            return render(request, "account/login.html",context)
        login(request, user)
        return redirect("show_url")
    return render(request, "account/login.html", {})


def logout_view(request):
    return render(request, "account/logout.html", {})

#def register_view(request):
#    return render(request, "account/register.html", {})

def createTodoView(request):
    form = TodoForm
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_url")
    template_name = "todoapp/todo.html"
    context = {"form": form}
    return render(request, template_name, context)

def showTodoView(request):
    obj = Todo.objects.all()
    template_name = "todoapp/show.html"
    context = {"obj": obj}
    return render(request, template_name, context)

def updateTodoView(request, f_id):
    obj = Todo.objects.get(id=f_id)
    form = TodoForm(instance=obj)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("show_url")
    template_name = "todoapp/todo.html"
    context = {"form": form}
    return render(request, template_name, context)

def deleteTodoView(request, f_id):
    obj = Todo.objects.get(id = f_id)
    if request.method == "POST":
        obj.delete()
        return redirect("show_url")
    template_name = "todoapp/confirmation.html"
    context = {"obj": obj}
    return render(request, template_name, context)


# Informations d'authentification Twilio

TWILIO_SID = 'ACb9ca8e54c6a75d9fd6a7f101ede91028'
TWILIO_AUTH_TOKEN = '869189b77afcc88d403cb7ccec2443cd'
TWILIO_PHONE_NUMBER = '+12564154251'

db_config = {
    'user': 'root',
    'password': 'Database@25',
    'host': 'localhost',
    'database': 'ol',
}

def envoyer_sms(Numero, message):
    """Envoie un SMS à un numéro de téléphone spécifique."""
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=Numero
        )
        print(f"Message envoyé à {Numero} avec SID : {sms.sid}")
        return sms.sid
    except Exception as e:
        print(f"Erreur lors de l'envoi du SMS à {Numero} : {e}")
        return None

def envoyer_sms_view(request, id):
    """Vue pour envoyer un SMS à un opérateur spécifique."""
    operator = get_object_or_404(Todo, id=id)  # Récupérer l'opérateur par ID
    Numero = operator.Numero
    Date_vm = operator.Date_vm


    if request.method == 'POST':
    # Formatage de la date pour l'inclure dans le message
        if Date_vm:
            date_formatee = Date_vm.strftime('%d/%m/%Y')
            time_formatee = Date_vm.strftime('%H:%M')  # Format de l'heure en 24h
            message = f"""Bonjour {operator.Nom},
            Nous vous rappelons que vous avez un rendez-vous médical prévu le {date_formatee} à {time_formatee} heures.
            Afin de confirmer votre présence, merci de répondre à ce message avec un OK.
            Sans réponse de votre part, le rendez-vous sera annulé.
            Cordialement."""
# Appel de la fonction d'envoi de SMS
            sms_sid = envoyer_sms(Numero, message)
            if sms_sid:
                return JsonResponse({'status': 'success', 'message': 'SMS envoyé!', 'sms_sid': sms_sid})
            else:
                return JsonResponse({'status': 'error', 'message': 'Échec de l\'envoi du SMS.'})

    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})
#"templates/envoi_sms.html",{}

