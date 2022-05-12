from django.contrib.auth.models import User, Group 

from rest_framework import serializers

from drf_tutorial.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# Гиперсвязывание - хороший REST-дизайн 
class QSUserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]

class QSGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ["url", "name"]

"""
    Сериализаторы позволяют преобразовывать данные из Json-а в экземпляры модели 
    и позволяет преобразовывать экземпляры модели в Json 

    Объявление сериализаторов работает приблизительно также, как и объявление форм
"""


