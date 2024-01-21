import base64
import io
import json
from typing import Dict, Any
import matplotlib.pyplot as plt
import requests as rqt

from django.contrib import messages
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from note_planner import forms
from .models import *
from note_planner_api.models import *
from .mixins import *


def get_user_headers(request):
    user_token = Token.objects.filter(user_id=request.user.id)
    if user_token.exists():
        user_token = user_token[0]

    headers = {'Authorization': f'Token {user_token}'}
    return headers


@method_decorator(login_required, name='dispatch')
class IndexPageView(View, TemplateColorsMixin):
    template_name = 'note_planner/index.html'

    def get(self, request):
        task_statistic_data = self.get_task_statistic(request)

        chart_labels = ['Высокий приоритет', 'Средний приоритет', 'Низкий приоритет']
        percents = task_statistic_data['tasks_priority_percents']
        colors = self.get_task_priority_colors_dict(request)

        if colors:
            colors = colors.values()

        pie_chart_64 = None
        # Создаём круговую диаграмму
        if percents:
            pie_chart_64 = self.create_circle_chart(request=request, labels=chart_labels, percentages=percents,
                                                    colors=colors)

        context = {
            'task_statistic_data': task_statistic_data,
            'pie_chart': pie_chart_64,
        }
        return render(request, self.template_name, context=context)

    @staticmethod
    def get_task_statistic(request) -> dict:
        task_data = Task.objects.filter(user=request.user)
        completed_task_data = task_data.filter(completed=1)

        count_task = task_data.count()
        count_completed_tasks = completed_task_data.count()
        avg_complete_time = None
        last_complete_task = completed_task_data.order_by('completed_at').last()

        h_p_percent = task_data.filter(priority=1).count()
        m_p_percent = task_data.filter(priority=2).count()
        l_p_percent = task_data.filter(priority=3).count()

        try:
            tasks_priority_percents = list(
                map(lambda x: round(x / count_task * 100, 1), (h_p_percent, m_p_percent, l_p_percent)))
        except:
            tasks_priority_percents = None
        temp_time_list = list()

        if completed_task_data:
            for task in completed_task_data:
                time_completed = task.completed_at - task.created_at
                temp_time_list.append(time_completed.seconds)

        if temp_time_list:
            avg_complete_time = sum(temp_time_list) // len(temp_time_list)

        return {
            'count_task': count_task,
            'completed_tasks': count_completed_tasks,
            'not_completed_tasks': count_task - count_completed_tasks,
            'avg_complete_time': avg_complete_time,
            'last_complete_task': last_complete_task,
            'tasks_priority_percents': tasks_priority_percents
        }

    @staticmethod
    def create_circle_chart(request, labels, percentages, colors):
        # Создание круговой диаграммы
        fig1, ax1 = plt.subplots()
        ax1.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)

        plt.title('Диаграмма количества задач по приоритету', color='white')
        for text in ax1.texts:
            text.set_color('white')

        # Установка равной оси, чтобы сделать круговую диаграмму круглой
        ax1.axis('equal')
        fig1.patch.set_alpha(0)

        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        # Кодирование изображения в base64
        image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

        # Очищаем текущий график (это необходимо, чтобы он не появлялся в следующем графике)
        plt.clf()

        return image_base64


@login_required
def notes_page(request):
    user = request.user

    existing_category = Category.objects.filter(name='Все', user=user).first()

    if not existing_category:
        # Если категории 'Все' нет, создаем новую
        latin_name = Category.custom_translit('Все')
        Category.objects.create(name='Все', latin_name=latin_name, user=user)

    category_data = Category.objects.all().filter(user=user)
    sorted_key = lambda x: x[0] != 'Все'  # функция для сортировки категорий для перемещения "Все" на первое место
    categories = sorted(((category.name, category.latin_name) for category in category_data), key=sorted_key)

    category_response = request.GET.get('category')

    form = forms.AddCategory(request.GET)
    notes_data = Note.objects.filter(user=user)
    notes = dict()

    for note in notes_data:
        if category_response == note.category.latin_name or category_response in ('Vse', None):
            notes[note.title] = {
                'content': note.content,
                'created_at': note.created_at,
                'id': note.id
            }

    context = {
        'notes_dict': notes,
        'categories_tuple': categories,
        'form': form
    }

    return render(request, 'note_planner/notes.html', context=context)


def delete_note_page(request, note_id):
    Note.objects.get(id=note_id).delete()

    return redirect('notes_page_path')


def delete_note_category(request):
    print(request.POST)
    if request.method == 'POST':
        form = forms.DeleteCategoryForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data['category_id'])
    return redirect('notes_page_path')


def add_note_page(request):
    user = request.user

    # Проверяем авторизован ли пользователь
    if not user.is_authenticated:
        return redirect('login_page_path')

    if request.method == 'POST':
        form = forms.NoteForm(user, request.POST)

        if form.is_valid():
            # Получаем данные из формы
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            category_name = form.cleaned_data['category']  # Получаем название категории из формы

            category = Category.objects.get(name=category_name, user=user)

            new_note = Note.objects.create(
                title=title,
                content=content,
                category=category,  # Передаем объект категории
                user=user  # Предполагаем, что заметка связана с текущим пользователем
            )
            return redirect('notes_page_path')
    else:
        form = forms.NoteForm(user)
    return render(request, 'note_planner/add_note.html', context={'form': form})


def add_note_category(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login_page_path')

    post_dict = request.POST
    category_name = post_dict.get('name')
    if category_name != '':
        latin_name = Category.custom_translit(category_name)
        # Проверяем существование категории с таким именем для данного пользователя
        existing_category = Category.objects.filter(name=category_name, user=user).first()

        if existing_category:
            # Категория уже существует, обработайте этот случай здесь
            pass
        else:
            # Категория не существует, создаем новую категорию
            Category.objects.create(name=category_name, latin_name=latin_name, user=user)

    return redirect('notes_page_path')


@method_decorator(login_required, name='dispatch')
class TasksPageView(View, TemplateColorsMixin):
    template_name = 'note_planner/tasks.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.task_api_endpoint = 'http://127.0.0.1:8000' + reverse('task_api_path-list')

    def get(self, request):
        context = {}

        headers = get_user_headers(request)

        try:
            task_response = rqt.get(self.task_api_endpoint, headers=headers)
            task_response.raise_for_status()
            # Фильтруем записи по параметру выполнено
            task_data = list(filter(lambda di: di['completed'] is False, task_response.json()))

            # Проходимся по задачам пользователя и добавляем подзадачи, если имеются
            for task in task_data:
                subtask_api_endpoint = self.task_api_endpoint + str(task['id']) + '/subtasks/'

                subtask_response = rqt.get(subtask_api_endpoint, headers=headers)
                subtask_response.raise_for_status()

                task['subtasks_list'] = subtask_response.json()

            context = {
                'len_tasks': len(task_data),
                'tasks_list': task_data,
                'add_task_form': forms.AddTaskForm(request.user),
                'add_subtask_form': forms.AddSubTaskForm()
            }
            # Получаем цвета для приоритета задач и добавляем их словарь context
            task_priority_colors = self.get_task_priority_colors_dict(request)
            if task_priority_colors is not None:
                context.update(task_priority_colors)

        except rqt.exceptions.RequestException as ex:
            messages.success(request, 'Произошла ошибка при получении данных')

        return render(request, self.template_name, context=context)

    def post(self, request, task_id=None):
        # Получаем заголовки запроса для пользователя
        headers = get_user_headers(request)

        # Достаём название пришедшей формы из скрытого поля
        form_type = request.POST.get('form_type')
        # Достаём название нажатой кнопки из пришедшей формы
        form_button = request.POST.get('button')

        if form_type == 'add_task':
            self.process_add_task_form(request, headers)

        if form_type == 'add_subtask':
            self.process_add_subtask_form(request, headers)

        if form_type == 'done_edit_delete_task_form' and task_id:

            if form_button == 'delete':
                self.process_delete_task(request, task_id, headers)

            elif form_button == 'done':
                self.process_switch_task(task_id, headers)

            elif form_button == 'edit':
                print('edit')

        if form_type == 'checkbox_form' and request.POST.getlist('checkbox'):

            if form_button == 'delete':
                for i in request.POST.getlist('checkbox'):
                    self.process_delete_task(request, int(i), headers)

            elif form_button == 'done':
                for i in request.POST.getlist('checkbox'):
                    self.process_switch_task(int(i), headers)

        if form_type == 'edit_subtask_form':
            if form_button == 'done':
                self.process_switch_subtask(request, headers)
            elif form_button == 'delete':
                self.process_delete_subtask(request, headers)

        return redirect('tasks_page_path')

    # Обработка формы добавления задачи
    def process_add_task_form(self, request, headers):
        add_task_form = forms.AddTaskForm(request.user, request.POST)

        if add_task_form.is_valid():
            task_data = add_task_form.cleaned_data
            task_data['user'] = request.user

            rqt.post(self.task_api_endpoint, data=task_data, headers=headers)
        else:
            return render(request, self.template_name, context={'add_task_form': add_task_form})

    # Обработка формы добавления подзадачи
    def process_add_subtask_form(self, request, headers):
        add_subtask_form = forms.AddSubTaskForm(request.POST)

        # Проверяем форму на валидность
        if add_subtask_form.is_valid() and add_subtask_form.cleaned_data['title']:
            # Получаем ID задачи, к которой относится подзадача
            task_id = request.POST.get('task_id')

            new_subtask_data = {'title': add_subtask_form.cleaned_data['title'],
                                'description': add_subtask_form.cleaned_data['description'],
                                'task': task_id}

            subtask_api_endpoint = self.task_api_endpoint + task_id + '/subtasks/'

            # Сохраняем подзадачу
            response = rqt.post(subtask_api_endpoint, data=new_subtask_data, headers=headers)

    def process_switch_task(self, task_id, headers):
        task_api_endpoint = self.task_api_endpoint + str(task_id) + '/'
        response = rqt.get(task_api_endpoint, headers=headers)
        response.raise_for_status()

        # Получаем словарь с данными о задаче
        task_data = response.json()
        if not task_data['completed']:
            task_data['completed_at'] = timezone.now()
        task_data['completed'] = not task_data['completed']  # Получаем статус и меняем его на противоположный
        rqt.put(task_api_endpoint, data=task_data, headers=headers)  # Обновляем данные через апи

    def process_switch_subtask(self, request, headers):
        task_id = request.POST.get('task_id')
        subtask_id = request.POST.get('subtask_id')

        # Формируем эндпоинт для delete запроса к апи
        subtask_api_endpoint = f'{self.task_api_endpoint}{task_id}/subtasks/{subtask_id}/'

        response = rqt.get(subtask_api_endpoint, headers=headers)
        response.raise_for_status()
        subtask = response.json()
        subtask_completed = subtask['completed']

        data = {'completed': not subtask_completed}
        response = rqt.patch(subtask_api_endpoint, data=data, headers=headers)
        response.raise_for_status()

        text = 'Подзадача ' + ['Выполнена', 'Активна'][subtask_completed]
        messages.success(request, text)

    def process_delete_task(self, request, task_id, headers):
        response = rqt.delete(f'{self.task_api_endpoint}{task_id}', headers=headers)
        response.raise_for_status()

        messages.success(request, 'Задача удалена')

    def process_delete_subtask(self, request, headers):
        task_id = request.POST.get('task_id')
        subtask_id = request.POST.get('subtask_id')

        # Формируем эндпоинт для delete запроса к апи
        subtask_api_endpoint = f'{self.task_api_endpoint}{task_id}/subtasks/{subtask_id}/'

        response = rqt.delete(subtask_api_endpoint, headers=headers)
        response.raise_for_status()

        messages.success(request, 'Подзадача удалена')


class ArchivePageView(View):
    template_name = 'note_planner/archive.html'

    def get(self, request):
        data = Task.objects.filter(completed=1)
        tasks = {task.title: {'due_date': task.due_date,
                              'completed_at': task.completed_at,
                              'task_id': task.id} for task in data}
        context = {
            'archive_tasks': tasks
        }
        return render(request, self.template_name, context=context)

    def post(self, request, task_id):
        form_type = request.POST.get('form_type')

        if form_type == 'archive_task_form' and task_id:
            form_button = request.POST.get('button')

            if form_button == 'delete-task':
                headers = get_user_headers(request)
                TasksPageView.process_delete_task(request, task_id, headers=headers)

            elif form_button == 'return-task':
                headers = get_user_headers(request)
                TasksPageView().process_switch_task(task_id, headers)
        return redirect('archive_page_path')


class LoginPageView(View):
    template_name = 'note_planner/registration/login.html'
    api_token_endpoint = 'http://127.0.0.1:8000/auth/token/login/'

    def get(self, request, context=None):
        form = forms.UserAuthenticationForm()
        if not context:
            context = {
                'form': form
            }
        return render(request, self.template_name, context)

    def post(self, request):
        form = forms.UserAuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Если пользователь существует делаем пост-запрос к эндпоинту для создания токена

                response = rqt.post(
                    self.api_token_endpoint,
                    data={'username': username, 'password': password}
                )
                # Если создание токена прошло успешно то логиним пользователя
                if response.status_code == 200:

                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('index_page_path')
                else:
                    print(response.data)
        return self.get(request, context={'form': form})


def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Создаём запись о пользователе в таблице настроек цвета
            TaskColorSettings(user=user).save()

            return redirect('notes_page_path')
    else:
        form = UserCreationForm()
    return render(request, 'note_planner/registration/register.html', context={'form': form})


def logout_page(request):
    api_token_endpoint = 'http://127.0.0.1:8000/auth/token/logout/'

    user_token = Token.objects.filter(user_id=request.user.id)

    if user_token.exists():
        user_token = user_token[0]
        # Если токен существует передаём его в пост запрос к апи для удаления
        response = rqt.post(api_token_endpoint, headers={'Authorization': f'Token {user_token}'})

    logout(request)
    messages.success(request, 'Вы вышли мз системы')

    return redirect('index_page_path')


@method_decorator(login_required, name='dispatch')
class UserSettingsView(View, TemplateColorsMixin):
    template_name = 'note_planner/settings/user_settings.html'

    @staticmethod
    def rgba_to_hex(r, g, b, a=255):
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        a = max(0, min(255, a))

        return "#{:02x}{:02x}{:02x}{:02x}".format(r, g, b, a)

    def get(self, request):
        context = self.get_task_priority_colors_dict(request)
        return render(request, self.template_name, context=context)

    def post(self, request):
        task_priority = request.POST.get('task_priority')
        if task_priority:
            r = int(request.POST.get('red'))
            g = int(request.POST.get('green'))
            b = int(request.POST.get('blue'))
            a = 255 - int(request.POST.get('alpha'))
            print(a)
            hex_color = self.rgba_to_hex(r, g, b, a)

            # Проверяем есть ли запись в БД, если нет,то создаём её
            if not self.get_task_priority_colors_dict(request):
                TaskColorSettings.objects.create(user=request.user, **{f'{task_priority}_priority_color': hex_color})
            else:
                TaskColorSettings.objects.update(user=request.user, **{f'{task_priority}_priority_color': hex_color})

        return redirect('settings_page_path')


class UserProfileView(View):
    template_name = 'note_planner/profile/user_profile.html'

    def get(self, request):
        user = User.objects.get(id=request.user.id)

        photo_form = forms.UploadUserPhotoForm()
        info_form = forms.UserProfileInfoFrom(instance=user)
        change_pass_form = forms.ChangeProfilePasswordFrom()

        context = {
            'photo_form': photo_form,
            'info_form': info_form,
            'change_pass_form': change_pass_form
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        upload_form = forms.UploadUserPhotoForm(request.POST, request.FILES)
        info_form = forms.UserProfileInfoFrom(request.POST)
        change_pass_form = forms.ChangeProfilePasswordFrom(request.POST)
        form_button = request.POST.get('button')

        if upload_form.is_valid():
            self.process_upload_photo(request, upload_form)

        elif info_form.is_valid() and form_button == 'change_info':
            self.process_change_user_info(request, info_form)
            messages.success(request, 'Изменено')

        elif change_pass_form.is_valid():
            self.process_change_user_password(request, change_pass_form)
            messages.success(request, 'Пароль успешно изменён')
            return redirect('user_profile_path')

        context = {
            'upload_form': upload_form,
            'info_form': info_form,
            'change_pass_form': change_pass_form,
        }

        return render(request, self.template_name, context=context)

    @staticmethod
    def process_upload_photo(request, form):
        photo = form.cleaned_data['photo']

        # Получаем старое фото и переключаем метку main_photo в False
        old_main_photo = UserProfilePhoto.objects.filter(user=request.user, main_photo=True)
        old_main_photo.update(main_photo=False)

        # Создаём новое основное фото профиля
        new_photo = UserProfilePhoto(photo=photo, user=request.user, main_photo=True)
        new_photo.save()

    @staticmethod
    def process_change_user_info(request, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']

        User.objects.filter(id=request.user.id).update(first_name=first_name, last_name=last_name, email=email)

    @staticmethod
    def process_change_user_password(request, form):
        password = form.cleaned_data['password']
        password_repeat = form.cleaned_data['password_repeat']
        if password == password_repeat:
            user = User.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()
            login(request, user)


class ChangeProfilePhotoView(View):
    def get(self, request):
        user_photo_data = UserProfilePhoto.objects.filter(user=request.user)

        contex = {'user_photos': user_photo_data}
        return render(request, 'note_planner/profile/choice_profile_photo.html', contex)

    def post(self, request):
        photo_id = request.POST.getlist('photo_id')
        form_button = request.POST.get('button')

        if photo_id:
            if form_button == 'change_photo':
                user_photo_data = UserProfilePhoto.objects.filter(user=request.user)
                user_photo_data.update(main_photo=False)

                user_photo = user_photo_data.filter(id=photo_id[-1])
                user_photo.update(main_photo=True)

            elif form_button == 'delete_photo':
                for id in photo_id:
                    UserProfilePhoto.objects.filter(user=request.user, id=id).delete()
                return redirect('change_profile_photo_path')

        return redirect('user_profile_path')
