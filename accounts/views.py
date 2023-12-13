from django.shortcuts import render,redirect

#Helps to create predefined forms (signup form--username,password1,password2)
#AuthenticationForm(username,password)
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

#Create user
from django.contrib.auth.models import User
#Helps to login,Logout,authenticate with username & password entered
from django.contrib.auth import login,logout,authenticate

#Integrity lets you uniquely identify column in database, if not uniquely identify IntegrityError is returned
from django.db import IntegrityError

#Makes login required otherwise show login page (LOGIN_URL in settings.py file)
from django.contrib.auth.decorators import login_required


# Create your views here.
def signupuser(request):
    #If signup link is opened, it's a GET request
    if request.method == 'GET':
        return render(request,'accounts/signup.html',{'form':UserCreationForm()})
    else:
        #Otherwise the request is POST(posting the details and clicking on sign up button)
        #Retrieving details
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if  password1 == password2:
            # Create a new user
            try:
                user = User.objects.create_user(username = username , password = password1)
                #Saving user into database
                user.save()
                #As soon as user signs up, it is logged in
                login(request,user)
                #After logging in, we need to show some page (currenttodos.html),redirecting to webpage
                return redirect('currenttodos')

            except IntegrityError:
                return render(request,'accounts/signup.html',{'form':UserCreationForm(),'error':'Username already exists!'})
        else:
            #If passwords does not match (return the same page again with additional details)
            return render(request,'accounts/signup.html',{'form':UserCreationForm(),'error':'Passwords didn\'t match'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        #Logouts the user
        logout(request)
        #returning to specific webpage
        return redirect('home')


def loginuser(request):
    #If signup link is opened, it's a GET request
    if request.method == 'GET':
        return render(request,'accounts/login.html',{'form':AuthenticationForm()})
    else:
        #Otherwise the request is POST(posting the details and clicking on Login button)
        #Retrieving details
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Authenticating the username and the password entered
        user = authenticate(request,username = username , password = password)

        #if user is not authenticated, user object returns None
        #We will send the same login page again but with an error
        if user is None:
            return render(request,'accounts/login.html',{'form':AuthenticationForm(),'error':'Username and Password didn\'t match'})
        else:
            #If user object is not empty, user is logged in successfully
            login(request,user)
            #After logging in, we need to show some page (currenttodos.html),redirecting to webpage
            return redirect('currenttodos')
