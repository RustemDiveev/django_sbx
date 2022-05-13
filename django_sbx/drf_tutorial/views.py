from django.contrib.auth.models import User, Group 
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status, generics, mixins 
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from drf_tutorial.serializers import QSGroupSerializer, QSUserSerializer, SnippetModelSerializer
from drf_tutorial.models import Snippet 

# Вместо множества представлений - общее поведение группируется во viewset
class QSUserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows user to be viewed or edited 
    """
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = QSUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class QSGroupViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = QSGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

"""
    Можно легко разбить viewset - на отдельные представления, 
    но viewset сохраняет логику представлений очень маленькой и предельно точной
"""

# Обычные представления Django 
@csrf_exempt
def snippet_list(request):
    """
        List all code snippets, or create a new snippet 
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser.parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # 201 - CREATED
            return JsonResponse(serializer.data, status=201)
        # 400 - BAD REQUEST 
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
        Retrieve, update or delete a code snippet 
    """
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == "GET":
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        snippet.delete()
        # 204 - NO CONTENT
        return HttpResponse(status=204)

"""
    Пишем обновленные вью на основании следующей информации

    У DRF есть Request, расширяющий функционал HttpRequest
    request.POST - обрабатывает только данные с формы и работает только для метода POST 
    request.data - обрабатывает произвольные данные, работает только для методов POST, PUT и PATCH 

    У DRF есть Response, который является типом TemplateResponse, принимающий неотрендеренный контент и 
    общающийся с контентом для определения типа контента, который надо вернуть на клиент 
    return Response(data) - отрисовывает тип контента по запросу клиента 

    Использование числовых статусов HTTP - не всегда очевидно.
    DRF предоставляет явные идентификаторы статусных кодов веб-сервера, что находятся в модуле status,
    например, HTTP_400_BAD_REQUEST 

    Также у DRF есть обертки для написании API-представлений:
    1. Декоратор @api_view для работы с представлениями, основанными на функции
    2. Класс APIView для работы с представлениями, основанными на классе 

    Эти обертки добавляют следующую функциональность:
    1. Дают гарантию, что на вход представлению приходит экземпляр Request из DRF 
    2. Добавляют контекст к объектам Response, чтобы можно было определить тип возвращаемого контента 
    3. Обертки также возвращают 405 Method Not Allowed, когда это требуется 
    4. Обертки обрабатывают исключения ParseError, когда происходит доступ к request.data, когда повреждаются входные данные 
"""

@api_view(["GET", "POST"])
def snippet_apiview_list(request):
    """
        List all code snippets or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def snippet_apiview_detail(request, pk):
    """
        Retrieve, update or delete a code snippet.
    """
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == "GET":
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = SnippetModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
    Добавление необязательных форматных суффиксов к URL
    Чтобы получить преимущество от того, что responses не привязаны к одному типу контента, 
    можно добавить поддержку форматных суффиксов к API endpoints. 

    Использование форматных суффиксов дает URL, которые явно ссылаются на определенный формат и означают, 
    что API сможет поддерживать URL следующего вида (т.е с форматом на конце):
    http://example.com/api/items/4.json
"""

@api_view(["GET", "POST"])
def snippet_format_list(request, format=None):
    """
        List all code snippets or create a new snippet.
    """
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def snippet_format_detail(request, pk, format=None):
    """
        Retrieve, update or delete a code snippet.
    """
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == "GET":
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = SnippetModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Использование class-based views 
# Дают лучшее разделение между различными методами HTTP
class SnippetList(APIView):
    """
        List all snippets, or create a new snippet 
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
        Retrieve, update or delete a snippet instance 
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Написание Class-based views с использованием классов-примесей 
class SnippetMixinList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SnippetMixinDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# Использование универсальных основанных на классах представлений 
class SnippetGenericList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

class SnippetGenericDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer
    