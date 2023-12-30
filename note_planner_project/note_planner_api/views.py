from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *
from .mixins import APIResponseMixin


# authentication_classes = [TokenAuthentication]
# permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Task.objects.filter(user=self.request.user).order_by('priority', '-created_at')

        return Task.objects.filter(user=self.request.user, id=pk)

    # Получаем подзадачи для конкретной задачи
    @action(methods=['get', 'post', 'delete'], detail=True)
    def subtasks(self, request, pk=None):
        # роут - task/{pk}/subtasks/

        task_instance = self.get_object()
        if request.method == 'GET':
            subtasks_data = SubTask.objects.filter(task=task_instance)
            serialized_data = SubtaskSerializer(subtasks_data, many=True).data
            return Response({'subtasks': serialized_data})

        elif request.method == 'POST':
            serializer = SubtaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(task=task_instance)  # Устанавливаем связь с родительской задачей
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'put', 'delete'], detail=True, url_path='subtasks/(?P<subtask_id>[^/.]+)')
    def subtask_detail(self, request, pk=None, subtask_id=None):
        task_instance = self.get_object()
        # Получение экземпляра подзадачи
        subtask_instance = get_object_or_404(SubTask, pk=subtask_id, task=task_instance)

        if request.method == 'GET':
            serializer = SubtaskSerializer(subtask_instance)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = SubtaskSerializer(subtask_instance, data=request.data)
            # Обновление данных подзадачи
            serializer = SubtaskSerializer(subtask_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            SubTask.objects.filter(id=subtask_id).delete()
            return Response({'success': 'Подзадача удалена'})


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Note.objects.filter(user=self.request.user)

        return Note.objects.filter(user=self.request.user, id=pk)




