from django.shortcuts import render
from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer,AnnouncementTitleSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
#from announcement.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'announcement': reverse('announcement-list', request=request, format=format),
    })

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    
    def list(self, request):
        '''
        only list {'id','url','owner', 'title'}
        '''
        queryset = Announcement.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AnnouncementTitleSerializer(page, many=True,context={'request': request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = AnnouncementTitleSerializer(queryset, many=True,context={'request': request})
            return Response(serializer.data)

    