from django.contrib.auth.models import User, Group 

from rest_framework import viewsets, permissions

from drf_tutorial.serializers import QSGroupSerializer, QSUserSerializer

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
