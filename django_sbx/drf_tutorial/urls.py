from django.urls import include, path 

from rest_framework import routers 

from drf_tutorial import views

router = routers.DefaultRouter()
router.register(r'users', views.QSUserViewSet)
router.register(r'groups', views.QSGroupViewSet)

"""
    Из-за того, что используется viewsets вместо views - 
    можно автоматически сгенерировать URLConf 
    путем регистрации viewset через класс router.
"""
urlpatterns = [
    path("qs", include(router.urls)),
    path("qs-api-auth", include("rest_framework.urls", namespace="rest_framework")),

    path("snippets/", views.SnippetCBListView.as_view()),
    path("snippets/<int:pk>/", views.SnippetCBListView.as_view()),
]