from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from note_planner_api.views import *


router = routers.SimpleRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'note', NoteViewSet, basename='note')


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', include('note_planner.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]

