from rest_framework.viewsets import ModelViewSet

from .models import House, Human, Phone, Contact 
from .serializers import HouseSerializer, HumanSerializer, PhoneSerializer, ContactSerializer


class HouseViewset(ModelViewSet):
    """
        Вьюсет для дома 
    """
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    # Эти два поля жизненно необходимы, чтобы сгенерировать правильную ссылку 
    # В нашем случае со slug, а не с pk на конце 
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class HumanViewset(ModelViewSet):
    """
        Вьюсет для человека 
    """
    queryset = Human.objects.all()
    serializer_class = HumanSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class PhoneViewset(ModelViewSet):
    """
        Вьюсет для телефона 
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"


class ContactViewset(ModelViewSet):
    """
        Вьюсет для телефонного контакта 
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
