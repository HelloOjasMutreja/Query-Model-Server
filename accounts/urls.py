from django.urls import path
from . import views

urlpatterns = [

    path('<str:username>/', views.userProfile, name='user_profile'),
    path('profile/edit/', views.editUser, name='edit_user'),

]