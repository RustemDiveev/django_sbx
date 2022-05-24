from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import HouseViewset, HumanViewset, PhoneViewset, ContactViewset

router = ExtendedDefaultRouter()

router.register("houses", HouseViewset)
router.register("humans", HumanViewset)
router.register("phones", PhoneViewset)
router.register("contacts", ContactViewset)

urlpatterns = router.urls

# Это важно, чтобы резолвить URL в сериализаторах 
app_name = "drf_nested_url"