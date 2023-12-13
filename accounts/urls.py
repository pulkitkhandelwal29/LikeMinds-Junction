from django.urls import path,include

from . import views

urlpatterns = [
    #Authentication
    path('signup',views.signupuser,name='signupuser'),
    path('logout',views.logoutuser,name='logoutuser'),
    path('login',views.loginuser,name='loginuser'),
]
