from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from apps.projects.models import Projects
from .models import Tasks, Subtasks, Comment, TaskLabel
from .forms import TaskForm, SubtaskForm, CommentForm, TaskLabelForm
# Create your views here.


@login_required
def task_list(request,project_pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    tasks = project.tasks.select_related('assignee', 'created_by').order_by('-created_at')
    task_counts = {status: 0 for status in Tasks.Status.values}
    for task in tasks:
        task_counts[task.status] += 1
    return render(request, 'tasks/task_list.html', {
        'project': project,
        'tasks': tasks,
        'task_counts': task_counts,
    })

@login_required
def task_detail(request, project_pk, pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)
    comment_form = CommentForm()
    return render(request, 'tasks/task_detail.html', {'project': project, 'task': task, 'comment_form': comment_form })

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.save()
            form.save_m2m()
            messages.success(request, f'Task "{task.title}" created')
            return redirect('tasks:detail', project_pk=project.pk, pk=task.pk)
    else:
        form = TaskForm(project=project)

    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})

@login_required
def task_update(request ,project_pk, pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated')
            return redirect('tasks:detail', project_pk=project.pk, pk=task.pk)
    else:
        form = TaskForm(instance=task, project=project)

    return render(request, 'tasks/task_form.html', {'form': form, 'project': project})


@login_required
@require_POST
def task_move(request, project_pk, pk):
    """Persist a drag-and-drop move from the task board."""
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)
    status = request.POST.get('status')
    valid_statuses = {choice.value for choice in Tasks.Status}

    if status not in valid_statuses:
        return JsonResponse({'error': 'Invalid task status.'}, status=400)

    if task.status != status:
        task.status = status
        task.save(update_fields=['status', 'updated_at'])

    return JsonResponse({'id': task.pk, 'status': task.status})

@login_required
def task_delete(request, project_pk, pk):
    project = get_object_or_404(Projects, pk=project_pk, owner=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)

    if request.method == 'POST':
        task.delete()
        messages.success(request, f'Task "{task.title}" deleted.')
        return redirect('tasks:list', project_pk=project.pk)

    return render(request, 'tasks/task_confirm_delete.html', {'task': task, 'project': project})


@login_required
def task_label_add(request, project_pk, pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            label, _ = TaskLabel.objects.get_or_create(name=name)
            task.labels.add(label)
        else:
            messages.error(request, 'Enter a label name.')
    return redirect('tasks:detail', project_pk=project.pk, pk=task.pk)


@login_required
def task_label_edit(request, project_pk, pk, label_pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)
    label = get_object_or_404(task.labels, pk=label_pk)
    form = TaskLabelForm(request.POST or None, instance=label)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task label updated.')
        return redirect('tasks:detail', project_pk=project.pk, pk=task.pk)
    return render(request, 'tasks/label_form.html', {'form': form, 'project': project, 'task': task, 'label': label})


@login_required
@require_POST
def task_label_remove(request, project_pk, pk, label_pk):
    project = get_object_or_404(Projects, pk=project_pk, members=request.user)
    task = get_object_or_404(Tasks, pk=pk, project=project)
    label = get_object_or_404(task.labels, pk=label_pk)
    task.labels.remove(label)
    messages.success(request, 'Label removed from task.')
    return redirect('tasks:detail', project_pk=project.pk, pk=task.pk)




@login_required
def subtask_create(request, task_pk):
    task = get_object_or_404(Tasks, pk=task_pk, project__members=request.user)

    if request.method == 'POST':
        form = SubtaskForm(request.POST)
        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.task = task
            subtask.save()
            return render(request, 'tasks/_subtask_row.html', {'subtask': subtask})
    else:
        form = SubtaskForm()

    return render(request, 'tasks/_subtask_form.html', {'form': form, 'task': task})


@login_required
def subtask_toggle(request, pk):
    subtask = get_object_or_404(Subtasks, pk=pk, task__project__members=request.user)
    subtask.is_completed = not subtask.is_completed
    subtask.save(update_fields=['is_completed', 'updated_at'])
    return render(request, 'tasks/_subtask_row.html', {'subtask': subtask})


@login_required
def subtask_delete(request, pk):
    subtask = get_object_or_404(Subtasks, pk=pk, task__project__members=request.user)
    subtask.delete()
    return HttpResponse('')  # HTMX swap target simply disappears



@login_required
def comment_create(request, task_pk):
    task = get_object_or_404(Tasks, pk=task_pk, project__members=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return render(request, 'tasks/_comment.html', {'comment': comment})

    return redirect('tasks:detail', project_pk=task.project.pk, pk=task.pk)

















