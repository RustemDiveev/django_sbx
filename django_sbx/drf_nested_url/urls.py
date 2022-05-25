from rest_framework_extensions.routers import ExtendedDefaultRouter

from .views import (
    HouseViewset, HumanViewset, PhoneViewset, ContactViewset,
    HumanNestedViewSet, PhoneNestedViewSet, ContactNestedViewSet
)

router = ExtendedDefaultRouter()

houses_router = router.register("houses", HouseViewset)
houses_router = houses_router.register(
    "humans", HumanNestedViewSet, 
    parents_query_lookups=["house_fk__slug"],
    basename="house-human"
)
houses_router = houses_router.register(
    "phones", PhoneNestedViewSet,
    parents_query_lookups=["human_fk__house_fk__slug", "human_fk__slug"],
    basename="house-human-phone"
)
houses_router = houses_router.register(
    "contacts", ContactNestedViewSet,
    parents_query_lookups=["phone_fk__human_fk__house_fk__slug", "phone_fk__human_fk__slug", "phone_fk__slug"],
    basename="house-human-phone-contact"
)

router.register("humans", HumanViewset)
router.register("phones", PhoneViewset)
router.register("contacts", ContactViewset)

urlpatterns = router.urls

# Это важно, чтобы резолвить URL в сериализаторах 
app_name = "drf_nested_url"