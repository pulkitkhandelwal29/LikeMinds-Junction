from django.urls import path,include

from . import views

urlpatterns = [
    path('current',views.currenttodos,name='currenttodos'),
    path('create',views.createtodo,name='createtodo'),
    path('findlikeminds',views.findlikeminds,name='findlikeminds'),
    path('report',views.report,name='report'),
    path('list/<int:todo_pk>',views.viewtodo,name='viewtodo'), #Listing the todo based on primary key (ID)
]

#Every link will come like 127.0.0.1/todo/current (etc.)
