from django.forms import ModelForm
from .models import project
from django.contrib.auth.models import User

class Project_form(ModelForm):
    class Meta:
        
        fields='__all__'
        model=project
        exclude=['host','participants']

class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username','email']
        
        
        

        