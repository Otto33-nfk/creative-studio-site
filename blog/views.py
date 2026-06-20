from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Comment
from .forms import ArticleForm


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.views += 1
    article.save()
    comments = article.comments.all()

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

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments
    })


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Статья опубликована!')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})


@login_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        messages.error(request, 'Нет доступа!')
        return redirect('article_list')
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Статья обновлена!')
            return redirect('profile')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        messages.error(request, 'Нет доступа!')
        return redirect('article_list')
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья удалена!')
        return redirect('profile')
    return render(request, 'confirm_delete.html', {
        'object': article,
        'type': 'статья'
    })