from rest_framework.serializers import ModelSerializer

from .models import TransactionTutorialModelDefault, TransactionTutorialModelAdditionalDB


class TransactionTutorialDefaultSerializer(ModelSerializer):

    class Meta:
        model = TransactionTutorialModelDefault
        fields = "__all__"


class TransactionTutorialAdditionalDBSerializer(ModelSerializer):

    class Meta:
        model = TransactionTutorialModelAdditionalDB
        fields = "__all__"
        