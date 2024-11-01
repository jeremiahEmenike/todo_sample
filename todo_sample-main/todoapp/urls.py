from django.urls import path
from . import views
#from accounts.views import login_view


urlpatterns = [
    #path('login/', views.login_view),
    path('', views.createTodoView, name='todo_url'),
    path('show/', views.showTodoView, name='show_url'),
    path('up/<int:f_id>', views.updateTodoView, name= 'update_url'),
    path('del/<int:f_id>', views.deleteTodoView, name= 'delete_url'),
    path('envoyer-sms/<int:id>/', views.envoyer_sms_view, name='envoyer_sms'),
]