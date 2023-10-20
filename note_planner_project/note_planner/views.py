from django.shortcuts import render
from .models import Note


def home_page(request):
    data = Note.objects.all()
    notes = {note.title: (note.content, note.created_at, note.category, note.user) for note in data}
    context = {
        'notes_dict': notes
    }
    return render(request, 'note_planner/index.html', context=context)

