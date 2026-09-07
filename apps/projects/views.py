from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Projects, ProjectMember
from .forms import ProjectForm, ProjectMemberForm
# Create your views here.


@login_required
def project_list(request):
    projects = Projects.objects.filter(members=request.user).order_by('-updated_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Projects, pk=pk, members=request.user)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()
            ProjectMember.objects.create(
                project=project,
                user=request.user,
                role=ProjectMember.Role.OWNER
            )
            messages.success(request, f'Project "{project.name}" created')
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Projects, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated')
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def member_add(request, project_pk):
    project = get_object_or_404(Projects, pk=project_pk, owner=request.user)

    if request.method == 'POST':
        form = ProjectMemberForm(request.POST, project=project)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()
            messages.success(request, f'{member.user} added to {project.name}')
            return redirect('projects:detail', pk=project_pk)
    else:
        form = ProjectMemberForm(project=project)
    return render(request, 'projects/member_form.html', {'form': form, 'project': project})

@login_required
def member_remove(request, project_pk,member_pk):
    project = get_object_or_404(Projects, pk=project_pk, owner=request.user)
    member = get_object_or_404(ProjectMember, pk=member_pk ,project=project)

    if member.role == ProjectMember.Role.OWNER:
        messages.error(request, "The project owner can't be removed. ")
        return redirect('projects:detail', pk=project.pk)

    if request.method == 'POST':
        member.delete()
        messages.success(request, f'{member.user} removed from {project.name}')
        return redirect('projects:detail', pk=project.pk)

    return render(request, 'projects/member_confirm_remove.html', {'member': member, 'project': project})









