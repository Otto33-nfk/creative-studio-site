from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Comment, ArticleLike
from .forms import ArticleForm


def article_list(request):
    articles = Article.objects.filter(status='approved')
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.status != 'approved':
        if not request.user.is_authenticated or (
            article.author != request.user and not request.user.is_staff
        ):
            messages.error(request, 'Эта статья пока недоступна.')
            return redirect('article_list')

    article.views += 1
    article.save()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        text = request.POST.get('text', '').strip()

        if text:
            Comment.objects.create(
                article=article,
                user=request.user,
                text=text
            )
            return redirect('article_detail', pk=pk)

    comments = article.comments.select_related('user')
    is_liked = False

    if request.user.is_authenticated:
        is_liked = ArticleLike.objects.filter(
            article=article,
            user=request.user
        ).exists()

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'is_liked': is_liked,
    })


@login_required
def toggle_article_like(request, pk):
    article = get_object_or_404(Article, pk=pk)

    like, created = ArticleLike.objects.get_or_create(
        article=article,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect('article_detail', pk=pk)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            if request.user.is_staff:
                article.status = 'approved'
                messages.success(request, 'Статья опубликована.')
            else:
                article.status = 'pending'
                messages.success(
                    request,
                    'Статья отправлена на модерацию. После одобрения она появится в блоге.'
                )

            article.save()
            return redirect('profile')
    else:
        form = ArticleForm()

    return render(request, 'add_article.html', {'form': form})


@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'Вы не можете редактировать чужую статью.')
        return redirect('profile')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save(commit=False)

            if request.user.is_staff:
                article.status = 'approved'
                messages.success(request, 'Статья обновлена.')
            else:
                article.status = 'pending'
                messages.success(
                    request,
                    'Статья обновлена и снова отправлена на модерацию.'
                )

            article.save()
            return redirect('profile')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'edit_article.html', {
        'form': form,
        'article': article
    })


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user and not request.user.is_staff:
        messages.error(request, 'Вы не можете удалить чужую статью.')
        return redirect('profile')

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена.')
        return redirect('profile')

    return render(request, 'confirm_delete.html', {
        'object': article,
        'type': 'статья'
    })