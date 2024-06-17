from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from taggit.models import TagBase, Tag, ItemBase

from datetime import date, datetime
import transliterate




class Task(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'PROG', 'In progress'
        IDLE = 'IDLE', 'Idle'

    name = models.CharField(max_length=100)
    detailed_descr = models.TextField(null=True, blank=True, verbose_name='description')
    slug = models.SlugField(max_length=100, unique_for_date='time_created')
    in_progress = models.CharField(max_length=4,
                                   choices=Status.choices,
                                   default=Status.IN_PROGRESS)
    created_by = models.ForeignKey(get_user_model(),
                                   on_delete=models.CASCADE,
                                   related_name='created_tasks',
                                   related_query_name='created_task',
                                   null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    time_to_finish = models.DateTimeField(null=True, blank=True)
    performers = models.ManyToManyField(get_user_model(),
                                        related_name='tasks',
                                        related_query_name='task')
    tags = TaggableManager(blank=True, related_name='tasks')

    objects = models.Manager()

    class Meta:
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['slug', 'time_created'])
        ]

    def __str__(self):
        return f'{self.name}: {self.detailed_descr[:10] if self.detailed_descr else ""}'

    def get_absolute_url(self):
        return reverse('tasks:tasks:page', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = transliterate.slugify(self.name) or self.name.lower().replace(' ', '-')
        count = Task.objects.exclude(pk=self.pk).filter(slug=self.slug).count()
        self.slug += str(count) if count else ''

        if self.time_to_finish and self.time_to_finish.date() < date.today():
            raise ValidationError("Date to finish couldn't be in the past")

        super(Task, self).save(*args, **kwargs)
