from django.db import models

"""
    We create 3 main tables in sbx_data_01  
    and STG_DELETE and STG for each of 3 tables in sbx_data_stg_01 
"""

class Breed(models.Model):
    """
        Breed - sbx_data_01 model
        catalog_one
    """
    name = models.CharField(max_length=100, unique=True)
    is_rare_flg = models.BooleanField()
    is_hunter_flg = models.BooleanField()


class Shelter(models.Model):
    """
        Shelter - sbx_data_01 model
        catalog_one
    """
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=200)
    address = models.TextField()
    

class Dog(models.Model):
    """
        Dog - sbx_data_01 model 
        catalog_two
    """
    name = models.CharField(max_length=100, unique=True)
    breed = models.ForeignKey(to=Breed, on_delete=models.PROTECT)
    age = models.PositiveIntegerField()
    shelter = models.ForeignKey(to=Shelter, on_delete=models.PROTECT)


class BreedStg(models.Model):
    """
        BreedStg - sbx_data_stg_01 model 
    """
    dml_operation_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    is_rare_flg = models.BooleanField()
    is_hunter_flg = models.BooleanField()

    class Meta:
        unique_together = (
            ("dml_operation_id", "name"),
        )


class BreedStgDelete(models.Model):
    """
        BreedStgDelete - sbx_data_stg_01 model
    """
    dml_operation_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = (
            ("dml_operation_id", "name"),
        )


class ShelterStg(models.Model):
    """
        ShelterStg - sbx_data_stg_01 model
    """
    dml_operation_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=200)
    address = models.TextField()

    class Meta:
        unique_together = (
            ("dml_operation_id", "name"),
        )


class ShelterStgDelete(models.Model):
    """
        ShelterStgDelete - sbx_data_stg_01 model 
    """
    dml_operation_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = (
            ("dml_operation_id", "name"),
        )


class DogStg(models.Model):
    """
        DogStg - sbx_data_stg_01 model 
    """
    dml_operation_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    shelter = models.CharField(max_length=100)

    class Meta:
        unique_together = (
            ("dml_operation_id", "name"),
        )


class DogStgDelete(models.Model):
    """
        DogStgDelete - sbx_data_stg_01 model 
    """
    dml_operation_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = (
            ("dml_operation_id", "name"),
        )
