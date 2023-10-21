from django.shortcuts import render
from .models import Note, Task, Category


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


def delete_note(request, note_id):
    Note.objects.get(id=note_id).delete()

    return notes_page(request)


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
