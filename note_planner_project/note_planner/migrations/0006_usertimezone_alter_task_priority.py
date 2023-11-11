# Generated by Django 4.2.6 on 2023-10-31 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note_planner', '0005_task_due_time_alter_task_due_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTimeZone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Высокий'), (2, 'Средний'), (3, 'Низкий')], default=3),
        ),
    ]
