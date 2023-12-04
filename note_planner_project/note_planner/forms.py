from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import FileExtensionValidator

from .models import *
from django.contrib.auth.models import User
from datetime import datetime


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100, required=True)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=True)


class NoteForm(forms.ModelForm):
    # Получаем queryset со значениями поля name из модели Category
    #
    # queryset = Category.objects.values_list('name', flat=True)
    # categories = list(queryset)
    # category = forms.ModelChoiceField(choices=categories, label='Выберите категорию')

    class Meta:
        model = Note
        fields = ['title', 'content', 'category']
        labels = {
            'title': 'Название',
            'content': 'Описание',
            'category': 'Выберите категорию'
        }

    def __init__(self, user, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        # Фильтруем queryset по полю user и сортируем
        self.fields['category'].queryset = Category.objects.filter(user=user)


class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    name = forms.CharField(max_length=100,
                           required=False,
                           widget=forms.TextInput(attrs={'class': 'input-add-category'}),
                           label='')


class UserAuthenticationForm(AuthenticationForm):
    model = User
    fields = ['username', 'password']


class DeleteCategoryForm(forms.Form):
    category_id = forms.IntegerField(widget=forms.HiddenInput())


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']


class AddTaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AddTaskForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        # Теперь вы можете использовать self.user в методе save() для доступа к пользователю
        task = super(AddTaskForm, self).save(commit=False)
        task.user = self.user
        if commit:
            task.save()
        return task

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'due_time', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'add-task-title'}),
            'description': forms.Textarea(attrs={'class': 'add-task-textarea'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'due-date-input'}),
            'due_time': forms.TimeInput(attrs={'type': 'time', 'class': 'due-time-input'}),
            'priority': forms.Select(attrs={'class': 'add-task-select-priority'})
        }
        labels = {
            'title': 'Название задачи',
            'description': 'Описание (не обязательно)',
            'due_date': 'Дата дедлайна',
            'due_time': 'Время (не обязательно)',
            'priority': 'Приоритет'
        }

        error_messages = {
            'title': {
                'required': 'Пожалуйста, введите название задачи.',
            },
            'due_date': {
                'required': 'Пожалуйста, выберите дату дедлайна.',
            },
            'priority': {
                'required': 'Пожалуйста, выберите приоритет.',
            },
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')

        if due_date and due_date < datetime.now().date():
            raise forms.ValidationError("Выберите дату, которая еще не прошла.")
        return due_date


class AddSubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = ['title', 'description']
        labels = {
            'title': 'Название подзадачи',
            'description': 'Описание (не обязательно)',
        }


class UploadUserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfilePhoto
        fields = ['photo']

    photo = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], label=''
    )

