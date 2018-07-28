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
from ojuser.models import *
from django.utils import timezone
from datetime import timedelta


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
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated,]
        if self.action == 'myanswers':
            self.permission_classes = [IsAuthenticated,]
        return super(self.__class__, self).get_permissions()

    ## user can only see his own answers
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

    def submit(self, request, pk):
        queryset = OJProblem.objects.all()
        p = get_object_or_404(queryset, pk=pk)

        owner = request.user
        delta = timezone.now() - owner.ojuserprofile.last_submit_time
        delta2 = timedelta(0, 10)
        # submit interval should longer than 10 seconds
        if delta < delta2:
            return errorResponse('submit too fast')
            
        serializer = SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            pass
        else:
            return errorResponse('input invalid')

        a = OJAnswer.objects.create(problem=p,
                                submitter=owner,
                                source_code=request.data['source_code'])
        # update last submit time
        profile = owner.ojuserprofile
        profile.last_submit_time = timezone.now()
        profile.save()
        # add count for current problem
        p.total_num += 1
        p.save()
        from tasks import judge
        judge.delay(a.id, p.id, owner.id, request.data['source_code'], p.input2, p.output2)
        return successResponse('submit success')


class OJRanksViewSet(viewsets.ModelViewSet):
    queryset = OJUserAnswerAggr.objects.all().order_by('-id')
    pagination_class = StandardResultsSetPagination
    serializer_class = AnswerRankSerializer

    def ranks(self, request, pk):
        queryset = OJUserAnswerAggr.objects.filter(problem__id=pk, result=0).order_by('cpu', 'memory')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)