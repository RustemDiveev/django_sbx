from random import randint

from django.db import models

class Person(models.Model):
    # Последовательность из двухразмерных кортежей: 1 - физическое значение, 2 - значение для отображения
    SHIRT_SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large")
    ]
    name = models.CharField(max_length=60)
    # Choices - домен возможных значений 
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)


class BlankNullModel(models.Model):
    """
        Для проверки blank и null
    """
    name = models.CharField(max_length=500)
    not_null_not_blank = models.CharField(max_length=1)
    null = models.CharField(max_length=1, null=True)
    blank = models.CharField(max_length=1, blank=True)
    blank_null = models.CharField(max_length=1, blank=True, null=True)


def default_callable_f():
    return "LITERAL"

def default_various_callable_f():
    return randint(1, 100)


class DefaultModel(models.Model):
    """
        Для проверки default 
    """
    default = models.CharField(max_length=10, default="TEST")
    default_callable = models.CharField(max_length=10, default=default_callable_f)
    default_various_callable = models.IntegerField(default=default_various_callable_f)
