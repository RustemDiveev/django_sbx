from django.db import models


class AbstractBaseModel(models.Model):
    """
        Абстрактный класс модели с полями аудита и технической версионности 
    """
    created_by = models.CharField("Пользователь, создавший запись", max_length=128, null=True) 
    created_dt = models.DateField("Дата создания записи", auto_now_add=True)
    created_dttm = models.DateTimeField("Дата и время создания записи", auto_now_add=True)
    modified_by = models.CharField("Пользователь, создавший запись", max_length=128, null=True) 
    modified_dt = models.DateField("Дата создания записи", auto_now=True)
    modified_dttm = models.DateTimeField("Дата и время создания записи", auto_now=True)

    def save(self, *args, **kwargs):
        self.created_by = "Creator"
        self.modified_by = "Modifier"
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class StaticModel(AbstractBaseModel):
    """
        Пример статической модели, наследующейся от абстрактной 
    """
    food_name = models.CharField("Название блюда", max_length=300)
    price=models.DecimalField("Цена блюда", max_digits=10, decimal_places=2)


def get_dynamic_model_v1():
    """
        Возвращает динамически сгенерированный класс модели 
    """

    class Meta:
        pass 

    setattr(Meta, "app_label", "audit_and_scd")

    attrs = {
        "name": models.CharField(max_length=100),
        "__module__": "audit_and_scd.models",
        "Meta": Meta,
    }

    return type("DynamicModelV1", (models.Model,), attrs)

def get_dynamic_model_v2():
    """
        Пытаемся наследоваться от абстрактной модели
    """

    class Meta:
        app_label="audit_and_scd"

    attrs={
        "name": models.CharField(max_length=100),
        "__module__": "audit_and_scd.models",
        "Meta": type("Meta", (), {"app_label": "audit_and_scd"})
    }

    return type("DynamicModelV2", (AbstractBaseModel,), attrs)


class UniqueTogetherSingleFieldModel(models.Model):
    name_1 = models.CharField(max_length=100, unique=True)
    name_2 = models.CharField(max_length=100)

    class Meta:
        unique_together = (
            ("name_1",),
            ("name_2",),
            ("name_1", "name_2"),
        )
        