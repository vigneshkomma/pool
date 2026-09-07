from django.contrib import admin
from .models import Projects, ProjectMember, ProjectLabel


# Register your models here.

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1



@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_id', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name',)
    inlines = [ProjectMemberInline]

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'user', 'role', 'joined_at')
    list_filter = ('role',)

@admin.register(ProjectLabel)
class AdminProjectLabel(admin.ModelAdmin):
    list_display = ('name',)

