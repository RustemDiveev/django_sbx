from .models import (
    Breed, Dog, Shelter, 
    BreedStg, BreedStgDelete,
    DogStg, DogStgDelete,
    ShelterStg, ShelterStgDelete
)

class PostprocessRouter:
    """
        Router to control all database operations for app Postprocess
    """

    data_db_models = (
        Breed, Dog, Shelter 
    )

    data_stg_db_models = (
        BreedStg, BreedStgDelete, 
        DogStg, DogStgDelete,
        ShelterStg, ShelterStgDelete
    )

    data_db_model_names, data_stg_db_model_names = (
        [model._meta.model_name for model in data_db_models],
        [model._meta.model_name for model in data_stg_db_models],
    )

    def db_for_read(self, model, **hints):
        db = None
        if model in self.data_db_models:
            db = "data"    
        elif model in self.data_stg_db_models:
            db = "data_stg"
        return None 

    def db_for_write(self, model, **hints):
        db = None
        if model in self.data_db_models:
            db = "data"    
        elif model in self.data_stg_db_models:
            db = "data_stg"
        return None  

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "postprocess":
            if db == "data" and model_name in self.data_db_model_names:
                return True 
            elif db == "data_stg" and model_name in self.data_stg_db_model_names:
                return True 
            elif db in ("pp_catalog_one") and model_name in ("catalogonemodel", "django_migrations"):
                return True
            elif db in ("pp_catalog_two") and model_name in ("catalogtwomodel", "django_migrations"):
                return True
            elif db in ("postprocess") and model_name in ("catalogonemodelwithmeta", "catalogtwomodelwithmeta"):
                return True
            else:
                return False 
        elif db in ("data", "data_stg"):
            return False
        else:
            return True
