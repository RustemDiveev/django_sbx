from django.db import transaction, DatabaseError

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action 
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import TransactionTutorialModelDefault, TransactionTutorialModelAdditionalDB
from .serializers import TransactionTutorialDefaultSerializer, TransactionTutorialAdditionalDBSerializer


class TransactionTutorialDefaultViewset(ModelViewSet):
    serializer_class = TransactionTutorialDefaultSerializer
    queryset = TransactionTutorialModelDefault.objects.all()



class TransactionTutorialAdditionalDBViewset(ModelViewSet):
    serializer_class = TransactionTutorialAdditionalDBSerializer
    queryset = TransactionTutorialModelAdditionalDB.objects.db_manager("additional_db").all()

    @action(detail=False, methods=["post"])
    def insert_data(self, request, *args, **kwargs):

        errors, serializers = [], []

        for obj in request.data:
            serializer = self.get_serializer(data=obj, partial=True)
            serializer.is_valid(raise_exception=True)
            serializers.append(serializer)

        try:
            with transaction.atomic(using="additional_db"):
                for row in serializers:
                    with transaction.atomic(using="additional_db"):
                        try:
                            row.save()
                        except DatabaseError as err:
                            errors.append(err.args[0])
                if errors:
                    raise DatabaseError("Transaction rollbacked")
        except DatabaseError as err:
            return Response({"status": "error", "errors": errors}, status=HTTP_400_BAD_REQUEST)

        return Response({"status": "success"}, status=HTTP_200_OK)


"""
пример вставляемых данных, вызывающих DatabaseError:
[
    {
        "attr_u": "B",
        "attr_nn": "B",
        "attr_ut_1": "B",
        "attr_ut_2": "B"
    }, 
    {
        "attr_u": "B",
        "attr_nn": "B",
        "attr_ut_1": "B",
        "attr_ut_2": "B"
    },
    {
        "attr_u": "C",
        "attr_nn": "C",
        "attr_ut_1": "C",
        "attr_ut_2": "C"
    },
    {
        "attr_u": "C",
        "attr_nn": "C",
        "attr_ut_1": "C",
        "attr_ut_2": "C"
    },
    {
        "attr_u": "D",
        "attr_nn": "D",
        "attr_ut_1": "D",
        "attr_ut_2": "D"
    },
    {
        "attr_u": "D",
        "attr_nn": "D",
        "attr_ut_1": "D",
        "attr_ut_2": "D"
    }
]
"""