from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('decision/<str:pk>/', views.decision, name="decision"),
    path('create-decision/', views.createDecision, name="create-decision"),
    path('update-decision/<str:pk>/', views.updateDecision, name="update-decision"),

]