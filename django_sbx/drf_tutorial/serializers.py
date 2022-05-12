from django.contrib.auth.models import User, Group 

from rest_framework import serializers

# Гиперсвязывание - хороший REST-дизайн 
class QSUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]

class QSGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ["url", "name"]
