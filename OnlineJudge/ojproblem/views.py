# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class OJProblemViewSet(viewsets.ModelViewSet):
    queryset = OJProblem.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated() and self.action == 'list':
            return ListAuthProblemSerializer
        else:
            return ListProblemSerializer
