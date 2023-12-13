from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length = 100)
    # memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # datecompleted = models.DateTimeField(null=True,blank=True)
    # important = models.BooleanField(default=False)
    #ForeignKey establishes relation with this todo and particular user
    user = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        '''__str__ is the name that is stored on admin page '''
        return str(self.user)



class UserLocation(models.Model):
    
    #ForeignKey establishes relation with this todo and particular user
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    user = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        '''__str__ is the name that is stored on admin page '''
        return str(self.user)
