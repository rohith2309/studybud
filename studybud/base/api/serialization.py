
from rest_framework import serializers
from base.models import project

class RoomSerilizer(serializers.ModelSerializer):
     class Meta:
         model=project
         fields='__all__'
         
        
        