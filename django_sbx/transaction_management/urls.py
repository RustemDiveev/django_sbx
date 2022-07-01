from django.urls import include, path 

from rest_framework import routers 

from .views import (
    TransactionTutorialDefaultViewset, 
    TransactionTutorialAdditionalDBViewset
)


router = routers.DefaultRouter()
router.register(r"default", TransactionTutorialDefaultViewset)
router.register(r"additional_db", TransactionTutorialAdditionalDBViewset)

urlpatterns = [
    path("", include(router.urls)),
]
