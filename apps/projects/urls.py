# apps/projects/urls.py
from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('create/', views.project_create, name='create'),
    path('<int:pk>/', views.project_detail, name='detail'),
    path('<int:pk>/edit/', views.project_update, name='update'),
    path('<int:project_pk>/members/add/', views.member_add, name='member_add'),
    path('<int:project_pk>/members/<int:member_pk>/remove/', views.member_remove, name='member_remove'),
]