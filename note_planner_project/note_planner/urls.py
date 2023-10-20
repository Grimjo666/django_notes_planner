from django.urls import path
from note_planner import views


urlpatterns = [
    path('', views.home_page, name='home_page_path')
]