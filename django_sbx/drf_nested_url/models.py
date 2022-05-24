from django.db import models

from django_extensions.db.fields import AutoSlugField

from .utilities import slugify_function

"""
    Концепт такой:
    Есть дом 
    - в нем несколько человек 
    - у каждого по несколько мобил 
    - у каждого телефона свои контакты 
"""

class House(models.Model):
    """
        Дом 
    """
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    slug = AutoSlugField(
        populate_from = ("name"),
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000,
        unique=True
    )

    def __str__(self):
        return f"<House: {self.name}>"

class Human(models.Model):
    """
        Человек
    """
    house_fk = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    slug = AutoSlugField(
        populate_from=("name", "surname"),
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000,
        unique=True
    )

    class Meta:
        unique_together = (
            ("name", "surname")
        )

    def __str__(self):
        return f"<Human: {self.name} {self.surname}>"


class Phone(models.Model):
    """
        Телефон
    """
    human_fk = models.ForeignKey(Human, on_delete=models.CASCADE)
    model = models.CharField(max_length=128)
    purchase_date = models.DateField()
    price = models.IntegerField()
    slug = AutoSlugField(
        populate_from="slug_populate_from",
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000,
        unique=True
    )

    class Meta:
        unique_together = (
            ("model", "purchase_date")
        )
    
    def slug_populate_from(self):
        """
            Для того, чтобы работало slug-поле 
            У нас есть дата, её надо насильно привести к строчному виду
        """
        return f"{self.model} {str(self.purchase_date)}"

    def __str__(self):
        return f"<Phone: {self.model} purchased on {str(self.purchase_date)}>"

    
class Contact(models.Model):
    """
        Телефонный контакт 
    """
    phone_fk = models.ForeignKey(Phone, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    slug = AutoSlugField(
        populate_from=("name", "surname", "phone_number"),
        slugify_function=slugify_function,
        overwrite=True,
        max_length=1000,
        unique=True
    )

    class Meta:
        unique_together = (
            ("name", "surname", "phone_number")
        )

    def __str__(self):
        return f"<Phone: {self.name} {self.surname} {self.phone_number}>"
