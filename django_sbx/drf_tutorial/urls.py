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

    path("snippets/", views.snippet_list),
    path("snippets/<int:pk>/", views.snippet_detail),
    
    path("api_snippets/", views.snippet_apiview_list),
    path("api_snippets/<int:pk>", views.snippet_apiview_detail),
]

"""
    При помощи httpie:
    pip install httpie 
    Можно проверять что вернет представление

    В моем примере это:
    http http://127.0.0.1:8000/drf/snippets/

    Либо через web-браузер
"""