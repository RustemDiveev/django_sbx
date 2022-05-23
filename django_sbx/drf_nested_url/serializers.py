from rest_framework.serializers import HyperlinkedModelSerializer

from .models import House, Human, Phone, Contact


class HouseSerializer(HyperlinkedModelSerializer):
    """
        Сериализатор для дома 
    """

    class Meta:
        model = House 


class HumanSerializer(HyperlinkedModelSerializer):
    """
        Сериализатор для человека 
    """

    class Meta:
        model = Human


class PhoneSerializer(HyperlinkedModelSerializer):
    """
        Сериализатор для телефона 
    """

    class Meta:
        model = Phone 


class ContactSerializer(HyperlinkedModelSerializer):
    """
        Сериализатор для телефонного контакта 
    """

    class Meta:
        model = Contact
