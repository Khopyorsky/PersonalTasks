# Generated by Django 5.0.6 on 2024-06-16 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_in_progress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-time_created']},
        ),
        migrations.AlterField(
            model_name='task',
            name='detailed_descr',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]
