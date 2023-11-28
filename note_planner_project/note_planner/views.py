from typing import Dict, Any

from django.shortcuts import render, redirect, Http404, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from datetime import datetime

from note_planner import forms


class CacheDict:
    def __init__(self):
        self.cache_dict = dict()

    def get_cache(self, key):
        if self.cache_dict.get(key, None):
            return self.cache_dict[key]

    def update_cache_value(self, key, value):
        if self.get_cache(key):
            self.cache_dict[key] = value + self.cache_dict[key]
        else:
            self.cache_dict[key] = value


class TemplateColorsMixin:
    @staticmethod
    def get_task_priority_colors_dict(request) -> dict[str, Any] | None:
        task_colors = TaskColorSettings.objects.all().filter(user=request.user)
        if task_colors.exists():
            high_priority = task_colors[0].high_priority_color
            medium_priority = task_colors[0].medium_priority_color
            low_priority = task_colors[0].low_priority_color
            context = {
                'high_priority': high_priority,
                'medium_priority': medium_priority,
                'low_priority': low_priority
            }
            return context
        return None


def index_page(request):
    return render(request, 'note_planner/index.html')


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
    notes_data = Note.objects.all().filter(user=user)
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
        self.user = None
        self.cache = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        tasks_data = Task.objects.all().filter(user=self.user, completed=0).order_by('priority')
        subtasks_data = SubTask.objects.filter(task__in=tasks_data)
        tasks_dict = dict()
        cache = CacheDict()

        # Проходимся по задачам пользователя и создаём словарь с данными
        for task in tasks_data:

            # Проходимся по списку подзадач
            subtasks_list = list()
            for sub in subtasks_data:

                # Проверяем связана ли подзадача с основной задачей
                if sub.task == task:
                    subtasks_list.append({'title': sub.title,
                                          'description': sub.description,
                                          'completed': sub.completed,
                                          'id': sub.id
                                          })

            # Проверяем на дубликаты названия задачи
            if task.title in tasks_dict:
                if not cache.get_cache(task.title):
                    cache.update_cache_value(task.title, 2)
                    task.title = task.title + ' (2)'
                else:
                    cache.update_cache_value(task.title, 1)
                    task.title = task.title + f' ({str(cache.get_cache(task.title))})'

            tasks_dict[task.title] = {'due_date': task.due_date,
                                      'description': task.description,
                                      'due_time': task.due_time,
                                      'priority': task.priority,
                                      'id': task.id,
                                      'subtasks_list': subtasks_list}
        context = {
            'len_tasks': len(tasks_dict),
            'tasks_dict': tasks_dict,
            'add_task_form': forms.AddTaskForm(self.user),
            'add_subtask_form': forms.AddSubTaskForm()
        }
        # Получаем цвета для приоритета задач и добавляем их словарь context
        context.update(self.get_task_priority_colors_dict(request))

        return render(request, self.template_name, context=context)

    def post(self, request, task_id=None):
        # Достаём название пришедшей формы из скрытого поля
        form_type = request.POST.get('form_type')
        # Достаём название нажатой кнопки из пришедшей формы
        form_button = request.POST.get('button')

        if form_type == 'add_task':
            self.process_add_task_form(request)

        if form_type == 'add_subtask':
            self.process_add_subtask_form(request)

        if form_type == 'done_edit_delete_task_form' and task_id:

            if form_button == 'delete':
                self.process_delete_task(request, task_id)

            elif form_button == 'done':
                self.process_done_task(request, int(task_id))

            elif form_button == 'edit':
                print('edit')

        if form_type == 'checkbox_form' and request.POST.getlist('checkbox'):

            if form_button == 'delete':
                for i in request.POST.getlist('checkbox'):
                    self.process_delete_task(request, int(i))

            elif form_button == 'done':
                for i in request.POST.getlist('checkbox'):
                    self.process_done_task(request, int(i))

        if form_type == 'edit_subtask_form':
            if form_button == 'done':
                self.process_switch_subtask(request, task_id)
            elif form_button == 'delete':
                self.delete_subtask(request, task_id)

        return redirect('tasks_page_path')

    # Обработка формы добавления задачи
    def process_add_task_form(self, request):
        add_task_form = forms.AddTaskForm(request.user, request.POST)
        if add_task_form.is_valid():
            add_task_form.save(commit=False)
            add_task_form.instance.user = request.user
            add_task_form.save()
        else:
            return render(request, self.template_name, context={'add_task_form': add_task_form})

    # Обработка формы добавления подзадачи
    @staticmethod
    def process_add_subtask_form(request):
        add_subtask_form = forms.AddSubTaskForm(request.POST)

        # Проверяем форму на валидность
        if add_subtask_form.is_valid() and add_subtask_form.cleaned_data['title']:
            # Получаем ID задачи, к которой относится подзадача
            task_id = request.POST.get('task_id')
            task_model = Task.objects.all().get(id=task_id)
            # Сохраняем подзадачу
            SubTask.objects.create(
                title=add_subtask_form.cleaned_data['title'],
                description=add_subtask_form.cleaned_data['description'],
                task=task_model
            )

    @staticmethod
    def process_done_task(request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.completed = True
        task.completed_at = timezone.now()
        task.save()

    @staticmethod
    def process_switch_subtask(request, subtask_id):
        if request.method == 'POST':
            subtask = get_object_or_404(SubTask, id=subtask_id)
            # Инвертируем значение поля completed
            subtask.completed = not subtask.completed
            # Сохраняем изменения
            subtask.save()

    @staticmethod
    def process_delete_task(request, task_id):
        Task.objects.filter(user=request.user, id=task_id).delete()

    @staticmethod
    def delete_subtask(request, subtask_id):
        if request.method == 'POST':
            SubTask.objects.filter(id=subtask_id).delete()


class ArchivePageView(View):
    template_name = 'note_planner/archive.html'

    def get(self, request):
        data = Task.objects.all().filter(completed=1)
        tasks = {task.title: {'due_date': task.due_date,
                              'completed_at': task.completed_at,
                              'task_id': task.id} for task in data}
        context = {
            'archive_tasks': tasks
        }
        return render(request, self.template_name, context=context)

    def post(self, request, task_id=None):
        form_type = request.POST.get('form_type')
        if form_type == 'archive_delete_task_form' and task_id:
            TasksPageView.process_delete_task(request, task_id)

        return redirect('archive_page_path')


def login_page(request):
    if request.method == 'POST':
        form = forms.UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('index_page_path')

    else:
        form = forms.UserAuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'note_planner/registration/login.html', context=context)


def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes_page_path')
    else:
        form = UserCreationForm()
    return render(request, 'note_planner/registration/register.html', context={'form': form})


def logout_page(request):
    logout(request)

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
    template_name = 'note_planner/settings/user_profile.html'

    def get(self, request):
        form = forms.UploadUserPhotoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.UploadUserPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.cleaned_data['photo']
            new_photo = UserProfileInfo(photo=photo, user=request.user)
            new_photo.save()
            return redirect('user_profile_path')
        return render(request, self.template_name, {'form': form})
