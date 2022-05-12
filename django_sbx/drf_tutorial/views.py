from django.contrib.auth.models import User, Group 
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions
from rest_framework.parsers import JSONParser

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
# Что прикольно - кода для них нет ни в документации, ни в репозитории с обучающим приложением, поэтому пишу наобум 
class SnippetCBListView(ListView):
    """
        Class-based list view для Snippet 
    """
    model = Snippet
    template_name = "drf_tutorial/snippet_list.html"

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

class SnippetCBDetailView(DetailView):
    """
        Class based detail view для Snippet 
    """
    model = Snippet 
    template_name = "drf_tutorial/snippet_detail.html"

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
