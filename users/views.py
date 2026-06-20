from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Follow
from .forms import ProfileForm, UserUpdateForm
from main.models import PortfolioProject
from blog.models import Article


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    user_projects = PortfolioProject.objects.filter(author=request.user)
    user_articles = Article.objects.filter(author=request.user)

    return render(request, 'profile.html', {
        'profile': profile,
        'user_projects': user_projects,
        'user_articles': user_articles,
    })


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)

    projects = PortfolioProject.objects.filter(
        author=profile_user,
        status='approved'
    )
    articles = Article.objects.filter(
        author=profile_user,
        status='approved'
    )

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, 'public_profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'projects': projects,
        'articles': articles,
        'is_following': is_following,
    })


@login_required
def toggle_follow(request, username):
    following_user = get_object_or_404(User, username=username)

    if following_user == request.user:
        messages.error(request, 'Нельзя подписаться на самого себя.')
        return redirect('user_profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=following_user
    )

    if created:
        messages.success(request, f'Вы подписались на {following_user.username}.')
    else:
        follow.delete()
        messages.success(request, f'Вы отписались от {following_user.username}.')

    return redirect('user_profile', username=username)


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })