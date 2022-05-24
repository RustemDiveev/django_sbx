from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import HouseViewset, HumanViewset, PhoneViewset, ContactViewset

router = ExtendedDefaultRouter()

houses_router = router.register("houses", HouseViewset)
houses_router = houses_router.register(
    "humans", HumanViewset, 
    parents_query_lookups=["house_fk__slug"],
    basename="house-human"
)

router.register("humans", HumanViewset)
router.register("phones", PhoneViewset)
router.register("contacts", ContactViewset)

urlpatterns = router.urls

# Это важно, чтобы резолвить URL в сериализаторах 
app_name = "drf_nested_url"