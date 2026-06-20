from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('add/', views.add_article, name='add_article'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('<int:pk>/edit/', views.edit_article, name='edit_article'),
    path('<int:pk>/delete/', views.delete_article, name='delete_article'),
]