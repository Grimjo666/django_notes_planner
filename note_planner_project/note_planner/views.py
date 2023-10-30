from django.shortcuts import render, redirect, Http404
from .models import Note, Task, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from note_planner import forms


def index_page(request):
    user = request.user
    user_authenticated = True

    if not user.is_authenticated:
        user_authenticated = False

    context = {
        'user': user
    }
    return render(request, 'note_planner/index.html', context=context)


def notes_page(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login_page_path')

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


def tasks_page(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login_page_path')
    data = Task.objects.all()
    tasks = {task.title: {'due_date': task.due_date, 'priority': task.priority, 'id': task.id} for task in data if
             task.completed == 0}

    form = forms.UpdateTaskForm

    context = {
        'tasks_dict': tasks,
        'form': form
    }
    return render(request, 'note_planner/tasks.html', context=context)


def add_task(request):
    if request.method == 'POST':
        form = forms.AddTaskForm(request.POST)
        if form.is_valid():

            Task.objects.create(
                title=form.cleaned_data['title'],
                due_date=form.cleaned_data['due_date'],
                priority=form.cleaned_data['priority'],
                user=request.user
            )

            return redirect('tasks_page_path')

        return render(request, 'note_planner/add_task.html', context={'form': form})


def delete_task(request, task_id):
    if request.method == 'POST':
        Task.objects.filter(user=request.user, id=task_id).delete()
    return redirect('tasks_page_path')


def done_task(request, task_id):
    if request.method == 'POST':
        Task.objects.filter(user=request.user, id=task_id).update(completed=True)
        return redirect('tasks_page_path')


def archive_page(request):
    data = Task.objects.all()
    tasks = {task.title: (task.due_date, task.priority) for task in data if task.completed == 1}
    context = {
        'archive_tasks': tasks
    }
    return render(request, 'note_planner/archive.html', context=context)


def login_page(request):
    if request.method == 'POST':
        form = forms.UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
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
