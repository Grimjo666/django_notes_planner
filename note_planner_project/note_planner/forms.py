from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Note, Category, Task
from django.contrib.auth.models import User
from django.utils import timezone


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
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < timezone.now():
            raise forms.ValidationError("Выберите дату, которая еще не прошла.")
        return due_date
