from django.contrib import admin
from .models import Organisation

# Register your models here.

class Show_fields(admin.ModelAdmin):
	list_display= ['owner','name','country']

admin.site.register(Organisation , Show_fields)