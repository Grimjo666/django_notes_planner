from django.db import models
from django.contrib.auth.models import User
from transliterate import translit


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    latin_name = models.CharField(max_length=100, default='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def custom_translit(text):
        try:
            # Если текст является кириллическим
            result = translit(text, 'ru', reversed=True)
        except Exception:
            # Если текст не является кириллическим
            result = text
        return result

    def save(self, *args, **kwargs):
        self.latin_name = self.custom_translit(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Заметка: {self.title} | {self.category}'


class Task(models.Model):

    PRIORITY_CHOICES = [
        (1, 'Высокий'),
        (2, 'Средний'),
        (3, 'Низкий')
    ]

    title = models.CharField(max_length=100)
    due_date = models.DateField()
    due_time = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Задача: {self.title}'


class SubTask(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'Подзадача: {self.title}'

