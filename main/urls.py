from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/add/', views.add_project, name='add_project'),
    path('portfolio/<int:pk>/', views.project_detail, name='project_detail'),
    path('portfolio/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('portfolio/<int:pk>/delete/', views.delete_project, name='delete_project'),
]