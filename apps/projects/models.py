from django.db import models
from django.conf import settings
# Create your models here.

class ProjectLabel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Projects(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        ARCHIVED = 'ARCHIVED', 'Archived'
        COMPLETED = 'COMPLETED', 'Completed'


    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='projects'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMember',
        related_name='projects_joined'
    )
    labels = models.ManyToManyField(
        ProjectLabel,
        related_name='projects',
        blank=True
    )

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Owner'
        ADMIN = 'ADMIN', 'Admin'
        MEMBER = 'MEMBER', 'Member'

    project = models.ForeignKey(
        'Projects',
        on_delete=models.CASCADE,
        related_name='membership'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='project_membership'
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_member'
            )
        ]
        indexes = [
            models.Index(fields=['user'])
        ]

    def __str__(self):
        return f'{self.user} in {self.project} ({self.role})'










