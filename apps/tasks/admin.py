from django.contrib import admin

from apps.tasks.models import Tasks, Subtasks, Comment, TaskLabel


# Register your models here.

class SubtaskInline(admin.TabularInline):
    model = Subtasks
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Tasks)
class AdminTasks(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assignee', 'created_by', 'due_date')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title',)
    inlines = [SubtaskInline, CommentInline]

@admin.register(Subtasks)
class AdminSubtasks(admin.ModelAdmin):
    list_display = ('title', 'task', 'is_completed')
    list_filter = ('is_completed',)

@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ('task', 'author', 'content')

@admin.register(TaskLabel)
class AdminTaskLabel(admin.ModelAdmin):
    list_display = ('name',)