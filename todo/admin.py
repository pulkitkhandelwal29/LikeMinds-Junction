from django.contrib import admin

from .models import Todo, UserLocation

#There is field named 'created' in models
#Django Admin does not show it as it is automatically taken
#We show using this and reading as readonly_fields so that no one can edit it
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
# Register your models here

class UserLocationAdmin(admin.ModelAdmin):
	pass
    # readonly_fields = ('created',)
# Register your models here.

admin.site.register(Todo,TodoAdmin)
admin.site.register(UserLocation,UserLocationAdmin)