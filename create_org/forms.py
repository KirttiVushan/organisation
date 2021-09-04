from django.forms import ModelForm
from .models import Organisation 
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class Model_fields(ModelForm):


	class Meta:
		model=Organisation
		fields=['name','description','country','state','city','logo']
		exclude = ('user' ,)
		

class User_Add(ModelForm):

    class Meta:
        model=Organisation
        fields=['members']

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    


