from django.urls import path
from note_planner import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('', views.index_page, name='index_page_path'),
    path('', views.IndexPageView.as_view(), name='index_page_path'),
    path('login/', views.LoginPageView.as_view(), name='login_page_path'),
    path('register/', views.register_page, name='register_page_path'),
    path('logout/', views.logout_page, name='logout_path'),
    path('notes/', views.notes_page, name='notes_page_path'),
    path('delete_note/<int:note_id>/', views.delete_note_page, name='delete_note_page_path'),
    path('add_note/', views.add_note_page, name='add_note_page_path'),
    path('add_note_category/', views.add_note_category, name='add_note_category_page_path'),
    path('delete_note_category/', views.delete_note_category, name='delete_note_category_path'),
    path('tasks/', views.TasksPageView.as_view(), name='tasks_page_path'),
    path('tasks/<int:task_id>/', views.TasksPageView.as_view(), name='task_id_page_path'),
    path('archive/', views.ArchivePageView.as_view(), name='archive_page_path'),
    path('archive/<int:task_id>/', views.ArchivePageView.as_view(), name='task_id_archive_page_path'),
    path('settings/', views.UserSettingsView.as_view(), name='settings_page_path'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile_path'),
    path('profile/change_photo/', views.ChangeProfilePhotoView.as_view(), name='change_profile_photo_path')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)