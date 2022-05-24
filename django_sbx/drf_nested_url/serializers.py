from rest_framework import serializers

from .models import House, Human, Phone, Contact


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
            "url": {"view_name": "drf_nested_url:human-detail", "lookup_field": "slug"},
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
