from django import forms
from .models import Note, Category


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
                           label=''
                           )
