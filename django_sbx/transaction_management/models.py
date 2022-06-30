from enum import unique
from django.db import models


class TransactionTutorialModelDefault(models.Model):
    """
        Модель для проверки транзакционности - регаю в default
    """
    attr_u = models.CharField(max_length=100, unique=True, null=True)
    attr_nn = models.CharField(max_length=100, null=False)
    attr_ut_1 = models.CharField(max_length=100, null=True)
    attr_ut_2 = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (
            ("attr_ut_1", "attr_ut_2")
        )
        

class TransactionTutorialModelAdditionalDB(models.Model):
    """
        Модель для проверки транзакционности - регаю в additional_db
    """
    attr_u = models.CharField(max_length=100, unique=True, null=True)
    attr_nn = models.CharField(max_length=100, null=False)
    attr_ut_1 = models.CharField(max_length=100, null=True)
    attr_ut_2 = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = (
            ("attr_ut_1", "attr_ut_2")
        )