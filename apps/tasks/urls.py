from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [

    path('project/<int:project_pk>/tasks/', views.task_list, name='list'),
    path('project/<int:project_pk>/tasks/create/', views.task_create, name='create'),
    path('project/<int:project_pk>/tasks/<int:pk>/', views.task_detail, name='detail'),
    path('project/<int:project_pk>/tasks/<int:pk>/edit/', views.task_update, name='update'),
    path('project/<int:project_pk>/tasks/<int:pk>/delete/', views.task_delete, name='delete'),


    path('tasks/<int:task_pk>/subtasks/create/', views.subtask_create, name='subtask_create'),
    path('subtasks/<int:pk>/toggle/', views.subtask_toggle, name='subtask_toggle'),
    path('subtasks/<int:pk>/delete/', views.subtask_delete, name='subtask_delete'),

    path('tasks/<int:task_pk>/comments/create/', views.comment_create, name='comment_create'),
]