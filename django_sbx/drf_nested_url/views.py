from rest_framework.viewsets import ModelViewSet

from .models import House, Human, Phone, Contact 
from .serializers import HouseSerializer, HumanSerializer, PhoneSerializer, ContactSerializer


class HouseViewset(ModelViewSet):
    """
        Вьюсет для дома 
    """
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class HumanViewset(ModelViewSet):
    """
        Вьюсет для человека 
    """
    queryset = Human.objects.all()
    serializer_class = HumanSerializer


class PhoneViewset(ModelViewSet):
    """
        Вьюсет для телефона 
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class ContactViewset(ModelViewSet):
    """
        Вьюсет для телефонного контакта 
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
