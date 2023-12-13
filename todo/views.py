from django.shortcuts import render,redirect,get_object_or_404

#Forms created using django, importing the class name
from .forms import TodoForm

from django.contrib.auth.models import User

from geopy.distance import geodesic as GD

#Importing Todo from models to access all the todos created
from .models import Todo, UserLocation

from django.utils import timezone #Importing timezone to set datecompleted to NULL (fix the time as the curent time)

#Does not allow user to access page until user is logged in
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'todo/index.html')

@login_required
def currenttodos(request):
    #Accessing all todos for specific user that are in database
    #If the user clicks on completed that todo, it should not appear there (this is how it is a filter)
    todos = Todo.objects.filter(user = request.user)
    return render(request,'todo/currenttodos.html',{'todos':todos})

@login_required
def createtodo(request):
    #If createtodo link is opened, it's a GET request
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        #Put all the details recevied from webapge in TodoForm
        form = TodoForm(request.POST)
        #Save it but do not save right now in database(as user field is right now empty,we want the user to be attached)
        newtodo = form.save(commit = False)
        #Setting user to the user that is logged in
        newtodo.user = request.user
        #Now finally save it in database
        newtodo.save()
        #After saving todos, redirecting to the currenttodo webpage, where it can see its todos
        return redirect('currenttodos')

#Viewing todo based on Primary key
@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #accessing those todos only created by the specific user(prevent from someone just try to access todos by changing ID above in URL)
    if request.method == 'GET':
        form = TodoForm(instance=todo) #Calling the form with details already in it using instance of above todo
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        #Save the updated details
        form = TodoForm(request.POST,instance=todo) #Referring the instance of todo only that has saved info
        #Directly saving as no need to define which user
        form.save()
        return redirect('currenttodos')


@login_required
def findlikeminds(request):
    if request.method == 'GET':
        return render(request,'todo/findlikeminds.html')
    else:
        data = request.POST  # Assuming the data is sent via POST request
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location_details = UserLocation(latitude=latitude, longitude=longitude)
        location_details.user = request.user
        
        record = UserLocation.objects.filter(user_id=location_details.user_id)
        if record:
            record.update(
            latitude=latitude,
            longitude=longitude)
        else:
            location_details.save()


        return redirect('report')


def compare_locations(specific_user):
    # input_point = (latitude, longitude)
    friends = {}
    own_location_details= UserLocation.objects.filter(user_id=specific_user).values('user_id','latitude','longitude')
    own_interest_details = Todo.objects.filter(user_id=specific_user).values('user_id','title')
    # print(own_location_details[0]['latitude'])

    other_location_details= UserLocation.objects.values('user_id','latitude','longitude').exclude(user_id=specific_user)
    other_interest_details = Todo.objects.values('user_id','title').exclude(user_id=specific_user)
    
    # print(other_location_details[0]['user_id'])
    for i in other_interest_details:
        if own_interest_details[0]['title'] == i['title']:
            # print(i['title'])
            input_point = (own_location_details[0]['latitude'], own_location_details[0]['longitude'])
            # print(input_point)
            near_user = i['user_id']
            # print(near_user)
            for j in other_location_details:
                # print(j)
                if j['user_id'] == near_user:
                    # print('matched')
                    distance = (j['latitude'], j['longitude'])
                    # print(distance)
                    if GD(input_point, distance).km < 1:
                        near_distance = round(GD(input_point, distance).m)
                        # print(near_distance)
                        user = User.objects.get(id=near_user)
                        username = user.username
                        friends[username] = near_distance
                        # print(friends)
    return friends                         

@login_required
def report(request):
    if request.method == 'GET':
        current_user = request.user.id
        friends = compare_locations(current_user)
    return render(request,'todo/report.html',{'friends': friends})

# @login_required
# def completedtodos(request):
#     #Accessing all todos for specific user that are in database
#     #If the user wants to see completed todo, it should appear there (this is how it is a filter)
#     #Ordering in descending order (latest to not so latest) (using - sign)
#     todos = Todo.objects.filter(user = request.user , datecompleted__isnull = False).order_by('-datecompleted')
#     return render(request,'todo/completedtodos.html',{'todos':todos})

# @login_required
# def removecompletedtodo(request,todo_pk):
#     todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) #accessing those todos only created by the specific user(prevent from someone just try to access todos by changing ID above in URL)
#     if request.method == 'GET':
#         form = TodoForm(instance=todo) #Calling the form with details already in it using instance of above todo
#         return render(request,'todo/removecompletedtodo.html',{'todo':todo,'form':form})
