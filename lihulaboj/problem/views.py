from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from .models import Answser, Problem
from .serializers import AnswserSerializer, EditProblemSerializer, \
        ShowProblemSerializer, ListProblemSerializer, SubmitAnswerSerializer
from common import shortcuts, status


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    serializer_class = ListProblemSerializer

    def get_permissions(self):
        if self.action == 'edit':
            self.permission_classes = [IsAdminUser,]
        elif self.action == 'update':
            self.permission_classes = [IsAdminUser,]
        elif self.action == 'delete':
            self.permission_classes = [IsAdminUser,]
        return super(self.__class__, self).get_permissions()
    
    def edit(self, request):
        serializer = EditProblemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return shortcuts.success_response(status.NEW_PROBLEM_SUCCESS)
        else:
            return shortcuts.error_response(status.NEW_PROBLEM_FAILED)

    def update(self, request, pk):
        queryset = Problem.objects.all()
        problem = get_object_or_404(queryset, pk=pk)
        serializer = EditProblemSerializer(problem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return shortcuts.success_response(status.UPDATE_PROBLEM_SUCCESS)
        else:
            return shortcuts.error_response(status.UPDATE_PROBLEM_FAILED)

    def delete(self, request, pk):
        queryset = Problem.objects.all()
        problem = get_object_or_404(queryset, pk=pk)
        problem.delete()
        return shortcuts.success_response(status.DELETE_PROBLEM_SUCCESS)

    def detail(self, request, pk):
        queryset = Problem.objects.all()
        problem = get_object_or_404(queryset, pk=pk)
        problem_serializer = ShowProblemSerializer(problem)
        return shortcuts.success_response(problem_serializer.data)


class AnswserViewSet(viewsets.ModelViewSet):
    queryset = Answser.objects.all()
    serializer_class = AnswserSerializer

    def submit(self, request, problem_id):
        serializer = SubmitAnswerSerializer(data=request.data)
        if serializer.is_valid():
            queryset = Problem.objects.all()
            problem = get_object_or_404(queryset, pk=problem_id)
            author = request.user
            