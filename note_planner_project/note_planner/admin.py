from django.contrib import admin
from .models import *
from note_planner_api.models import *

admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)
