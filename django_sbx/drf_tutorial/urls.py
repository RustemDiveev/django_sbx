from django.urls import include, path 

from rest_framework import routers 
from rest_framework.urlpatterns import format_suffix_patterns

from drf_tutorial import views

router = routers.DefaultRouter()
router.register(r'users', views.QSUserViewSet)
router.register(r'groups', views.QSGroupViewSet)

# Поддержка URL с форматом 
# Здесь - внимание - можно выполнять format_suffix_patterns только над теми представлениями, где определен формат
urlpatterns_formated = [
    path("format_snippets/", views.snippet_format_list),
    path("format_snippets/<int:pk>/", views.snippet_format_detail),

    path("cbv_snippets/", views.SnippetList.as_view()),
    path("cbv_snippets/<int:pk>/", views.SnippetDetail.as_view()),

    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),

    path("auth_snippets/", views.SnippetAuthPermList.as_view(), name="snippet-list"),
    path("auth_snippets/<int:pk>/", views.SnippetAuthPermDetail.as_view(), name="snippet-detail"),

    path("", views.api_root),
    path("auth_snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),
]
urlpatterns_formated = format_suffix_patterns(urlpatterns_formated)

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
    path("api_snippets/<int:pk>/", views.snippet_apiview_detail),

    path("mixin_snippets/", views.SnippetMixinList.as_view()),
    path("mixin_snippets/<int:pk>/", views.SnippetMixinDetail.as_view()),
] + urlpatterns_formated

"""
    При помощи httpie:
    pip install httpie 
    Можно проверять что вернет представление

    В моем примере это:
    http http://127.0.0.1:8000/drf/snippets/

    Либо через web-браузер
"""

"""
    Вследствие добавления форматных суффиксов можно делать следующее:
    
    1. Можно также получить список всех элементов как и раньше 
    http http://127.0.0.1:8000/drf/format_snippets/

    2. Можно контролировать формат получаемого ответа используя заголовок Accept 
    http http://127.0.0.1:8000/drf/format_snippets/ Accept:application/json 
    http http://127.0.0.1:8000/drf/format_snippets/ Accept:text/html

    3. Или то же самое при помощи добавления форматного суффикса 
    http  http://127.0.0.1:8000/drf/format_snippets.json 
    http  http://127.0.0.1:8000/drf/format_snippets.api

    4. Также можно контролировать формат посылаемого запроса используя заголовок Content-Type 
    Здесь используются данные формы 
    http --form POST http://127.0.0.1:8080/drf/format_snippets/ code="print(123)"

    Здесь используется POST через JSON 
    http --json POST http://127.0.0.1:8080/drf/format_snippets/ code="print(456)"

    При выполнении 4-го пункта у меня возвращается WinError 10061 - как поправить я не понял пока.

    При помощи флага --debug можно увидеть тип запроса в заголовке запроса
"""

"""
    С учетом того, что настроена аутентфикация теперь - неавторизованному пользователю нельзя добавлять новые сниппеты 
    http POST http://127.0.0.1:8000/drf/auth_snippets/ code="print(123)"

    Можно вставить сниппет, если добавить пароль и логин пользователя 
    http -a django-admin:AIX8klidp POST http://127.0.0.1:8000/drf/auth_snippets/ code="print('Django's admin snippet')"
"""

"""
    Корневое API - ссылается на user-list и snippet-list 
    Сериализатор сниппета ссылается на snippet-highlight 
    Сериализатор пользователя включает поле, которое ссылается на snippet-detail 
    Сериализаторы сниппета и пользователя включают в себя поля url, которые по умолчанию ссылаются на 
        {model_name}-detail, которые в итоге будут snippet-detail, user-detail 
"""