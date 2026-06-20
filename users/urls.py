from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('u/<str:username>/', views.user_profile, name='user_profile'),
    path('u/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
]