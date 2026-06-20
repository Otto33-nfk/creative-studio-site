from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PortfolioProject
from .forms import ProjectForm


def home(request):
    projects = PortfolioProject.objects.all()[:3]
    return render(request, 'home.html', {'projects': projects})


def about(request):
    return render(request, 'about.html')


def contacts(request):
    return render(request, 'contacts.html')


def portfolio(request):
    projects = PortfolioProject.objects.all()
    return render(request, 'portfolio.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)
    project.views += 1
    project.save()
    return render(request, 'project_detail.html', {'project': project})


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, 'Проект успешно добавлен!')
            return redirect('portfolio')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)
    # Проверяем что это проект именно этого пользователя
    if project.author != request.user:
        messages.error(request, 'Нет доступа!')
        return redirect('portfolio')
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект обновлён!')
            return redirect('profile')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form, 'project': project})


@login_required
def delete_project(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)
    # Проверяем что это проект именно этого пользователя
    if project.author != request.user:
        messages.error(request, 'Нет доступа!')
        return redirect('portfolio')
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект удалён!')
        return redirect('profile')
    return render(request, 'confirm_delete.html', {
        'object': project,
        'type': 'проект'
    })