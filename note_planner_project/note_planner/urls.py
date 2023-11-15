from django.urls import path
from note_planner import views
from django.views.generic import TemplateView


urlpatterns = [
    # path('', views.index_page, name='index_page_path'),
    path('', TemplateView.as_view(template_name='note_planner/index.html'), name='index_page_path'),
    path('login', views.login_page, name='login_page_path'),
    path('register', views.register_page, name='register_page_path'),
    path('logout', views.logout_page, name='logout'),
    path('notes', views.notes_page, name='notes_page_path'),
    path('delete_note/<int:note_id>', views.delete_note_page, name='delete_note_page_path'),
    path('add_note', views.add_note_page, name='add_note_page_path'),
    path('add_note_category', views.add_note_category, name='add_note_category_page_path'),
    path('delete_note_category', views.delete_note_category, name='delete_note_category_path'),
    path('tasks', views.TasksPageView.as_view(), name='tasks_page_path'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task_path'),
    path('delete_subtask/<int:subtask_id>', views.delete_subtask, name='delete_subtask_path'),
    path('done_task/<int:task_id>', views.done_task, name='done_task_path'),
    path('switch_task/<int:subtask_id>', views.switch_subtask, name='done_subtask_path'),
    path('archive', views.archive_page, name='archive_page_path'),
    path('settings', views.UserSettingsView.as_view(), name='settings_page_path')
]