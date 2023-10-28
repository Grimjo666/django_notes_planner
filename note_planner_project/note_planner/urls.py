from django.urls import path
from note_planner import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', views.index_page, name='index_page_path'),
    path('login', views.login_page, name='login_page_path'),
    path('register', views.register_page, name='register_page_path'),
    path('logout', views.logout_page, name='logout'),
    path('notes', views.notes_page, name='notes_page_path'),
    path('delete_note/<int:note_id>', views.delete_note_page, name='delete_note_page_path'),
    path('add_note', views.add_note_page, name='add_note_page_path'),
    path('add_note_category', views.add_note_category, name='add_note_category_page_path'),
    path('tasks', views.tasks_page, name='tasks_page_path'),
    path('archive', views.archive_page, name='archive_page_path')
]