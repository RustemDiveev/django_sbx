from rest_framework import serializers
from rest_framework.reverse import reverse 

from .models import House, Human, Phone, Contact
from .utilities import MultipleLookupsHyperLinkedIdentityField


class HouseSerializer(serializers.HyperlinkedModelSerializer):
    """
        Сериализатор для дома 
    """
    humans = serializers.HyperlinkedIdentityField(
        view_name="drf_nested_url:house-human-list",
        lookup_field="slug",
        lookup_url_kwarg="parent_lookup_house_fk__slug"
    )

    class Meta:
        model = House 
        fields = ("slug", "url", "name", "address", "humans")
        extra_kwargs = {
            "url": {"view_name": "drf_nested_url:house-detail", "lookup_field": "slug"}
        }


class HumanSerializer(serializers.HyperlinkedModelSerializer):
    """
        Сериализатор для человека 
    """

    class Meta:
        model = Human
        fields = ("slug", "url", "house_fk", "name", "surname")
        # Для FK приходится дублировать extra_kwargs
        extra_kwargs = {
            "url": {"view_name": "drf_nested_url:house-human", "lookup_field": "slug"},
            "house_fk": {"view_name": "drf_nested_url:house-detail", "lookup_field": "slug"}
        }


class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    """
        Сериализатор для телефона 
    """

    class Meta:
        model = Phone 
        fields = ("slug", "url", "human_fk", "model", "purchase_date", "price")
        extra_kwargs = {
            "url": {"view_name": "drf_nested_url:phone-detail", "lookup_field": "slug"},
            "human_fk": {"view_name": "drf_nested_url:human-detail", "lookup_field": "slug"}
        }


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    """
        Сериализатор для телефонного контакта 
    """

    class Meta:
        model = Contact
        fields = ("slug", "url", "phone_fk", "name", "surname", "phone_number")
        extra_kwargs = {
            "url": {"view_name": "drf_nested_url:contact-detail", "lookup_field": "slug"},
            "phone_fk": {"view_name": "drf_nested_url:phone-detail", "lookup_field": "slug"}
        }


class HumanHyperLink(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            "parent_lookup_house_fk__slug": obj.house_fk.slug,
            "slug": obj.slug
        }

        return reverse(viewname=view_name, kwargs=url_kwargs, request=request, format=format)


class HumanNestedSerializer(serializers.HyperlinkedModelSerializer):
    """
        Вложенный сериализатор для человека 
    """
    url = HumanHyperLink(view_name="drf_nested_url:house-human-detail")
    phones = MultipleLookupsHyperLinkedIdentityField(
        view_name="drf_nested_url:house-human-phone-list",
        lookup_fields=(
            ("house_fk.slug", "parent_lookup_human_fk__house_fk__slug"), ("slug", "parent_lookup_human_fk__slug")
        )
    )
    
    class Meta:
        model = Human
        fields = ("slug", "url", "name", "surname", "phones")


class PhoneHyperLink(serializers.HyperlinkedIdentityField):

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            "parent_lookup_human_fk__house_fk__slug": obj.human_fk.house_fk.slug,
            "parent_lookup_human_fk__slug": obj.human_fk.slug,
            "slug": obj.slug
        }

        return reverse(viewname=view_name, kwargs=url_kwargs, request=request, format=format)


class PhoneNestedSerializer(serializers.HyperlinkedModelSerializer):
    """
        Вложенный сериализатор для телефона 
    """
    url = PhoneHyperLink(view_name="drf_nested_url:house-human-phone-detail")
    contacts = MultipleLookupsHyperLinkedIdentityField(
        view_name="drf_nested_url:house-human-phone-contact-list",
        lookup_fields=(
            ("human_fk.house_fk.slug", "parent_lookup_phone_fk__human_fk__house_fk__slug"),
            ("human_fk.slug", "parent_lookup_phone_fk__human_fk__slug"),
            ("slug", "parent_lookup_phone_fk__slug")
        )
    )
    
    class Meta:
        model = Phone 
        fields = ("slug", "url", "model", "purchase_date", "price", "contacts")


class ContactHyperLink(serializers.HyperlinkedIdentityField):
    
    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            "parent_lookup_phone_fk__human_fk__house_fk__slug": obj.phone_fk.human_fk.house_fk.slug,
            "parent_lookup_phone_fk__human_fk__slug": obj.phone_fk.human_fk.slug,
            "parent_lookup_phone_fk__slug": obj.phone_fk.slug,
            "slug": obj.slug
        }

        return reverse(viewname=view_name, kwargs=url_kwargs, request=request, format=format)


class ContactNestedSerializer(serializers.HyperlinkedModelSerializer):
    """
        Вложенный сериализатор для контактного номера 
    """
    url = ContactHyperLink(view_name="drf_nested_url:house-human-phone-contact-detail")
    
    class Meta:
        model = Contact 
        fields = ("slug", "url", "name", "surname", "phone_number")
