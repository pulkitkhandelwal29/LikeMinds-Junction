#Creating form
from django.forms import ModelForm

#Importing the models file created (that has forms)
from .models import Todo

class TodoForm(ModelForm):
    class Meta:
        #Accessing the class from models.py file
        model = Todo
        #Creating all the form fields that we want from models (these fields are defined in models.py file)
        fields = ['title']

#After this automatically forms get created with these fields
