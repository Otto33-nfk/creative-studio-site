from django.contrib import admin
from .models import PortfolioProject, ContactMessage, ProjectLike, ProjectComment


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'views', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'author__username']
    list_editable = ['status']


@admin.register(ProjectLike)
class ProjectLikeAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'created_at']
    search_fields = ['project__title', 'user__username']


@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'created_at']
    search_fields = ['project__title', 'user__username', 'text']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']