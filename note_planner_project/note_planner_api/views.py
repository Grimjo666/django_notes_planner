from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *


# authentication_classes = [TokenAuthentication]
# permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Task.objects.filter(user=self.request.user)

        return Task.objects.filter(user=self.request.user, id=pk)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Note.objects.filter(user=self.request.user)

        return Note.objects.filter(user=self.request.user, id=pk)




