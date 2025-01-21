from django.shortcuts import render
from rest_framework.generics import ListAPIView
from apps.oaauth.models import OADepartment
from apps.oaauth.serializers import DepartmentSerializer

# ListAPIView：仅提供get查询list，需求也是如此，不需要使用增删改，所以不使用ModelViewSet
class DepartmentListView(ListAPIView):
    queryset = OADepartment.objects.all()
    serializer_class = DepartmentSerializer