from django.shortcuts import render, redirect, Http404
from .models import Note, Task, Category
from django.contrib.auth.models import User
from .forms import RegistrationForm, NoteForm, AddCategory


def notes_page(request):
    user = request.user

    Category.objects.get_or_create(
        user=user,
        name='Все',
        defaults={'latin_name': Category.custom_translit('Все')}  # Если объект создается, задаем дополнительные поля
    )

    category_data = Category.objects.all().filter(user=user)
    sorted_key = lambda x: x[0] != 'Все'  # функция для сортировки категорий для перемещения "Все" на первое место
    categories = sorted(((category.name, category.latin_name) for category in category_data), key=sorted_key)

    category_response = request.GET.get('category')

    if category_response == 'add-category':
        pass
    form = AddCategory(request.GET)
    notes_data = Note.objects.all()
    notes = dict()

    for note in notes_data:
        if category_response == note.category.latin_name or category_response in ('vse', None):
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


def add_note_page(request):
    user = request.user

    # Проверяем авторизован ли пользователь
    if user.is_authenticated:

        if request.method == 'POST':
            form = NoteForm(user, request.POST)

            if form.is_valid():
                # Получаем данные из формы
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                category_name = form.cleaned_data['category']  # Получаем название категории из формы

                if category_name is None:
                    category_name = 'Все'

                try:
                    category = Category.objects.get(name=category_name)
                except:
                    latin_name = Category.custom_translit(category_name)  # Переводим имя категории
                    category = Category.objects.create(name=category_name, latin_name=latin_name, user=user)

                new_note = Note.objects.create(
                    title=title,
                    content=content,
                    category=category,  # Передаем объект категории
                    user=user  # Предполагаем, что заметка связана с текущим пользователем
                )
                return redirect('notes_page_path')
        else:
            form = NoteForm(user)
        return render(request, 'note_planner/add_note.html', context={'form': form})
    else:
        return redirect('login_page_path')


def add_note_category(request):
    user = request.user
    if user.is_authenticated:
        post_dict = request.POST
        category_name = post_dict.get('name')
        if category_name != '':
            latin_name = Category.custom_translit(category_name)
            Category.objects.create(name=category_name, latin_name=latin_name, user=user)

        return redirect('notes_page_path')
    else:
        return redirect('login_page_path')


def tasks_page(request):
    data = Task.objects.all()
    tasks = {task.title: (task.due_date, task.priority) for task in data if task.completed == 0}
    context = {
        'tasks_dict': tasks
    }
    return render(request, 'note_planner/tasks.html', context=context)


def archive_page(request):
    data = Task.objects.all()
    tasks = {task.title: (task.due_date, task.priority) for task in data if task.completed == 1}
    context = {
        'archive_tasks': tasks
    }
    return render(request, 'note_planner/archive.html', context=context)


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('Пользователь зарегистрирован')
    else:
        form = RegistrationForm
    return render(request, 'register.html', context={'form': form})
