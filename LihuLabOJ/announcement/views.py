from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer,AnnouncementTitleSerializer
from rest_framework import permissions,pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from common import shortcuts
from collections import OrderedDict
from announcement.permissions import IsOwnerOrReadOnly

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    #max_page_size = 1000

class AnnouncementList(generics.GenericAPIView):
    """
    List all Announcements, or create a new Announcement.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request,*args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer =  AnnouncementTitleSerializer(page, many=True,context={'request': request})
            return self.get_paginated_response(serializer.data)
            #return shortcuts.success_response(serializer.data)
        else:
            serializer = AnnouncementTitleSerializer(page, many=True,context={'request': request})
            return shortcuts.success_response(serializer.data)

    def post(self, request,*args, **kwargs):
        serializer = AnnouncementSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return shortcuts.success_response("Create announcement success.",
                                              status=status.HTTP_201_CREATED)
        return shortcuts.error_response(serializer.errors,
                                        status=status.HTTP_400_BAD_REQUEST)

class AnnouncementDetail(generics.GenericAPIView):
    """
    Retrieve, update or delete a Announcement instance.
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            return None



    def get(self, request, pk, format=None):
        Announcement = self.get_object(pk)
        if Announcement is not None:
            serializer = self.get_serializer(Announcement)
            return shortcuts.success_response(serializer.data)
        else:
            return shortcuts.error_response('The announcement doesnt exist.',
                                      status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        Announcement = self.get_object(pk)
        if Announcement is not None:
            serializer = self.get_serializer(Announcement,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return shortcuts.success_response("Upgrade announcement success.")
            return shortcuts.error_response(serializer.errors, 
                                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return shortcuts.error_response(serializer.errors)

    def delete(self, request, pk, format=None):
        Announcement = self.get_object(pk)
        if Announcement is not None:
            Announcement.delete()
            return shortcuts.success_response("Delete announcement success.")
        else:
            return shortcuts.error_response('The announcement doesnt exist.',
                                      status=status.HTTP_404_NOT_FOUND)