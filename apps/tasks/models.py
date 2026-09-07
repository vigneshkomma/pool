from django.db import models
from django.conf import settings
# Create your models here.


class TaskLabel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    class Status(models.TextChoices):
        TO_DO = 'TO_DO', 'To_do'
        IN_PROGRESS = 'IN_PROGRESS', 'In_progress'
        DONE = 'DONE', 'Done'
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    project = models.ForeignKey(
        'projects.Projects',
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TO_DO
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_tasks'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='created_tasks'
    )

    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    labels = models.ManyToManyField(
        TaskLabel,
        related_name='tasks',
        blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['project', 'status'])
        ]

    def __str__(self):
        return self.title

class Subtasks(models.Model):
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )

    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'comment by {self.author} on {self.task}'

















