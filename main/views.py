from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PortfolioProject, ProjectLike, ProjectComment
from .forms import ProjectForm, ContactForm


def home(request):
    projects = PortfolioProject.objects.filter(status='approved')[:3]
    return render(request, 'home.html', {'projects': projects})


def about(request):
    return render(request, 'about.html')


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Сообщение отправлено. Мы свяжемся с вами в ближайшее время.'
            )
            return redirect('contacts')
    else:
        form = ContactForm()

    return render(request, 'contacts.html', {'form': form})


def portfolio(request):
    projects = PortfolioProject.objects.filter(status='approved')
    return render(request, 'portfolio.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)

    if project.status != 'approved':
        if not request.user.is_authenticated or (
            project.author != request.user and not request.user.is_staff
        ):
            messages.error(request, 'Этот проект пока недоступен.')
            return redirect('portfolio')

    project.views += 1
    project.save()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        text = request.POST.get('text', '').strip()

        if text:
            ProjectComment.objects.create(
                project=project,
                user=request.user,
                text=text
            )
            return redirect('project_detail', pk=pk)

    comments = project.comments.select_related('user')
    is_liked = False

    if request.user.is_authenticated:
        is_liked = ProjectLike.objects.filter(
            project=project,
            user=request.user
        ).exists()

    return render(request, 'project_detail.html', {
        'project': project,
        'comments': comments,
        'is_liked': is_liked,
    })


@login_required
def toggle_project_like(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)

    like, created = ProjectLike.objects.get_or_create(
        project=project,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect('project_detail', pk=pk)


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user

            if request.user.is_staff:
                project.status = 'approved'
                messages.success(request, 'Проект опубликован.')
            else:
                project.status = 'pending'
                messages.success(
                    request,
                    'Проект отправлен на модерацию. После одобрения он появится в портфолио.'
                )

            project.save()
            return redirect('profile')
    else:
        form = ProjectForm()

    return render(request, 'add_project.html', {'form': form})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)

    if project.author != request.user and not request.user.is_staff:
        messages.error(request, 'Вы не можете редактировать чужой проект.')
        return redirect('profile')

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)

        if form.is_valid():
            project = form.save(commit=False)

            if request.user.is_staff:
                project.status = 'approved'
                messages.success(request, 'Проект обновлён.')
            else:
                project.status = 'pending'
                messages.success(
                    request,
                    'Проект обновлён и снова отправлен на модерацию.'
                )

            project.save()
            return redirect('profile')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'edit_project.html', {
        'form': form,
        'project': project
    })


@login_required
def delete_project(request, pk):
    project = get_object_or_404(PortfolioProject, pk=pk)

    if project.author != request.user and not request.user.is_staff:
        messages.error(request, 'Вы не можете удалить чужой проект.')
        return redirect('profile')

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Проект удалён.')
        return redirect('profile')

    return render(request, 'confirm_delete.html', {
        'object': project,
        'type': 'проект'
    })