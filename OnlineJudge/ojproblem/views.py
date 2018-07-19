# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *
from common.shortcuts import *


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

    def retrieve(self, request, pk):
        queryset = OJProblem.objects.all()
        problem = get_object_or_404(queryset, pk=pk)
        serializer = ShowProblemDetailSerializer(problem)
        return successResponse(serializer.data)


class OJAnswerViewSet(viewsets.ModelViewSet):
    queryset = OJAnswer.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    serializer_class = AnswerSerializer

    def get_permissions(self):
        if self.action == 'submit':
            self.permission_classes = [IsAuthenticated,]
        if self.action == 'detail':
            self.permission_classes = [IsAuthenticated,]
        if self.action == 'myanswers':
            self.permission_classes = [IsAuthenticated,]
        return super(self.__class__, self).get_permissions()

    ## user can only self answer
    def retrieve(self, request, pk):
        queryset = OJAnswer.objects.filter(submitter=request.user)
        answer = get_object_or_404(queryset, pk=pk)
        serializer = AnswerSerializer(answer)
        return successResponse(serializer.data)

    def myanswers(self, request, *args, **kwargs):
        queryset = OJAnswer.objects.filter(submitter=request.user).order_by('-id')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)