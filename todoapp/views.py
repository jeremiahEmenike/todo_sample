from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import TodoForm
from .models import Todo
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import mysql.connector


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
TWILIO_AUTH_TOKEN = '7fd5a7d7e6eb315ccda02fdd0300870f'
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

def bouton_sms_view(request):
    """Vue appelée par le bouton pour exécuter le script et envoyer un SMS avec la date."""
    if request.method == 'POST':
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Récupération de la date de l'événement pour le message
        requete = 'SELECT Numero, Date_vm FROM todoapp_todo WHERE Date_vm'
        cursor.execute(requete)
        resultat = cursor.fetchone()

        if resultat:
            Numero, Date_vm = resultat
            # Formatage de la date pour l'inclure dans le message
            date_formatee = Date_vm.strftime('%d/%m/%Y')
            
            message = """Bonjour,
            Nous vous rappelons que vous avez un rendez-vous médical prévu{date_formatee}.
            Afin de confirmer votre présence merci de répondre à ce message avec un OK
            Sans reponse de votre part le rendez-vous sera annulé
            Cordialement"""

            # Appel de la fonction d'envoi de SMS avec le message formaté
            sms_sid = envoyer_sms(Numero, message)

            # Fermeture de la connexion à la base de données
            conn.close()

            # Vérification du succès de l'envoi et réponse JSON
            if sms_sid:
                return JsonResponse({'status': 'success', 'message': f'SMS envoyé, SID: {sms_sid}'})
            else:
                return JsonResponse({'status': 'error', 'message': "Échec de l'envoi du SMS"})
        else:
            conn.close()
            return JsonResponse({'status': 'error', 'message': "Aucun événement trouvé pour cet utilisateur"})

    # Si la requête n'est pas POST, renvoie le template du bouton
    return render(request, envoyer_sms(Numero, message))

#"templates/envoi_sms.html",{}

