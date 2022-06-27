from dataclasses import Field
from django.db import models, connection 
from django.db.utils import ProgrammingError
from django.utils import timezone 

from pymongo import MongoClient 
from model_utils import FieldTracker


class AbstractSCDTracker(models.Model):

    created_by = models.CharField(max_length=128)
    created_dttm = models.DateTimeField()
    modified_by = models.CharField(max_length=128, null=True)
    modified_dttm = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        user, dttm = (
            kwargs.pop("user", None), 
            kwargs.pop("dttm", timezone.now())
        )
        pk_value = getattr(self, self._meta.pk.name)

        # update 
        if pk_value:
            self.modified_by = user 
            self.modified_dttm = dttm
            
            client = MongoClient("localhost", 27017)
            collection = client.test[self.__class__.__name__] 
            row = self.get_data_dict(before_changes=True)
            row.update({"modified_to_dttm": dttm})
            collection.insert_one(row)

        # insert
        else:
            self.created_by = user 
            self.created_dttm = dttm 

        super().save(*args, **kwargs)   

    def delete(self, *args, **kwargs):
        user, dttm = (
            kwargs.pop("user", None), 
            kwargs.pop("dttm", timezone.now())
        )

        client = MongoClient("localhost", 27017)
        collection = client.test[self.__class__.__name__]
        row = self.get_data_dict()
        row.update({"modified_to_dttm": dttm, "deleted_by": user})
        collection.insert_one(row)

        super().save(*args, **kwargs)

    def get_fields(self) -> list:
        return [field.name for field in self._meta.fields]

    def get_data_dict(self, before_changes: bool=False) -> dict:
        data = {}

        for field in self.get_fields():
            data.update({field: getattr(self, field)})

        if before_changes:
            data.update(self.tracker.changed())

        return data


def get_hardcoded_model():

    meta_attributes = {
        "app_label": "audit_and_scd",
        "constraints": [
            models.UniqueConstraint(fields=["pk_field"], name="SCDModelV2_dummy_pk")
        ]
    }

    fields = {
        "pk_field": models.CharField(max_length=1),
        "attr": models.CharField(max_length=100),
    }

    attributes = {
        "__module__": "audit_and_scd.scd",
        "Meta": type("Meta", (), meta_attributes),
        "tracker": FieldTracker()
    }
    attributes.update(fields)

    return type("SCDModelV2", (AbstractSCDTracker,), attributes)


def register_model(model):

    with connection.schema_editor() as db:
        try:
            db.delete_model(model)
        except ProgrammingError:
            pass 
    
    with connection.schema_editor() as db:
        db.create_model(model)

     