from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import get_current_authenticated_user

from datetime import date
import transliterate


# TODO: check if it works right
class ForUserManager(models.Manager):
    def get_queryset(self):
        user = get_current_authenticated_user()
        return super().get_queryset().filter(performers=user) if user else None


class Task(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'PROG', 'In progress'
        IDLE = 'IDLE', 'Idle'

    name = models.CharField(max_length=100)
    detailed_descr = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique_for_date='time_created')
    in_progress = models.CharField(max_length=4,
                                   choices=Status.choices,
                                   default=Status.IN_PROGRESS)
    created_by = CurrentUserField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    time_to_finish = models.DateTimeField(null=True, blank=True)
    performers = models.ManyToManyField(get_user_model(),
                                        related_name='tasks',
                                        related_query_name='task')

    objects = models.Manager()
    for_user = ForUserManager()

    class Meta:
        ordering = ['-time_created']
        indexes = [
            models.Index(fields=['slug', 'time_created'])
        ]

    def save(self, *args, **kwargs):
        self.slug = transliterate.slugify(self.name) or self.name.lower()
        count = Task.objects.filter(slug=self.slug).count()
        self.slug += str(count) if count else ''

        if self.time_to_finish and self.time_to_finish.date() < date.today():
            raise ValidationError("Date to finish couldn't be in the past")

        current_user = get_current_authenticated_user()
        if current_user and current_user not in self.performers:
            self.performers.add(current_user)

        super(Task, self).save(*args, **kwargs)
