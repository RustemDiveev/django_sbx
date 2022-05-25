from rest_framework.viewsets import ModelViewSet

from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import House, Human, Phone, Contact 
from .serializers import (
    HouseSerializer, HumanSerializer, PhoneSerializer, ContactSerializer,
    HumanNestedSerializer, PhoneNestedSerializer
)


class HouseViewset(NestedViewSetMixin, ModelViewSet):
    """
        Вьюсет для дома 
    """
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    # Эти два поля жизненно необходимы, чтобы сгенерировать правильную ссылку 
    # В нашем случае со slug, а не с pk на конце 

    """
        Поле из модели, по которому происходит поиск отдельных экземпляров модели 
        По умолчанию - 'pk'
        При использовании hyperlinked api необходимо удостовериться, что и представление,
        и сериализатор используют это же поле 
    """
    lookup_field = "slug"
    """
        Именованный аргумент для URL, который необходимо использовать для поиска объекта
        Конфигурация URL должна включать в себя данный именованный аргумент с этим значением.
        Если не указан, то принимает такое же значение, как и lookup field
    """
    lookup_url_kwarg = "slug"


class HumanViewset(ModelViewSet):
    """
        Вьюсет для человека 
    """
    queryset = Human.objects.all()
    serializer_class = HumanSerializer
    lookup_field = "slug"


class PhoneViewset(ModelViewSet):
    """
        Вьюсет для телефона 
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    lookup_field = "slug"


class ContactViewset(ModelViewSet):
    """
        Вьюсет для телефонного контакта 
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = "slug"


class HumanNestedViewSet(NestedViewSetMixin, ModelViewSet):
    """
        Вложенный вьюсет для человека 
    """
    queryset = Human.objects.all()
    serializer_class = HumanNestedSerializer
    lookup_field = "slug"
    lookup_kwargs = "parent_lookup_house_fk__slug"


class PhoneNestedViewSet(NestedViewSetMixin, ModelViewSet):
    """
        Вложенный вьюсет для телефона 
    """
    queryset = Phone.objects.all()
    serializer_class = PhoneNestedSerializer
    lookup_field = "slug"
