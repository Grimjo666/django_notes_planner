from django.shortcuts import render, redirect, Http404
from .models import Note, Task, Category
from django.contrib.auth.models import User
from .forms import RegistrationForm


def notes_page(request):
    category_data = Category.objects.all()
    categories = ((category.name, category.latin_name) for category in category_data)

    category_response = request.GET.get('category')

    notes_data = Note.objects.all()
    notes = dict()
    for note in notes_data:
        if category_response == note.category.latin_name or category_response in ('all', None):
            notes[note.title] = {
                'content': note.content,
                'created_at': note.created_at,
                'id': note.id
            }

    context = {
        'notes_dict': notes,
        'categories_tuple': categories,
    }

    return render(request, 'note_planner/notes.html', context=context)


def delete_note_page(request, note_id):
    Note.objects.get(id=note_id).delete()

    return redirect('notes_page_path')


def add_note_page(request):
    category_data = Category.objects.all()

    # Проверяем авторизован ли пользователь
    if request.user.is_authenticated:
        context = {
            'category_data': category_data,
        }

        return render(request, 'note_planner/add_note.html', context=context)
    else:
        return render(request, 'note_planner/login.html')


def save_note(request):
    post_dict = request.POST
    title = post_dict.get('title')
    content = post_dict.get('content')
    category_id = post_dict.get('category_id')
    print(title, category_id, content)

    return redirect('notes_page_path')


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
