from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('feed', views.feed, name="feed"),
    path('saved', views.savedDecisions, name="saved"),
    
    path('quick-decision/<str:pk>/', views.quickDecision, name='quick-decision'),
    path('create-decision/', views.createQuickDecision, name="create-quick-decision"),
    path('update-decision/<str:pk>/', views.updateQuickDecision, name="update-quick-decision"),
    path('delete-decision/<str:pk>/', views.deleteDecision, name="delete-decision"),

    path('public-decision/<str:pk>/', views.publicDecision, name='public-decision'),
    path('ask-people/', views.createPublicDecision, name="create-public-decision"),
    path('create-public-decision/<int:pk>/', views.updatePublicDecision, name='update-public-decision'),
    
    path('delete-option/<str:pk>/', views.deleteOption, name="delete-option"),
    path('decision/<int:pk>/random/', views.randomOption, name='random-option'),

    path('filter-decisions/', views.filter_decisions, name='filter_decisions'),
    path('recommend/', views.recommendations, name='recommend'),

    path('daily-decisions/', views.daily_decisions, name='daily-decisions'),
    path('decision/<int:pk>/set-daily-decision/', views.set_daily_decision, name='set-daily-decision'),
    path('decision/<int:pk>/unset-daily-decision/', views.unset_daily_decision, name='unset-daily-decision'),

    path('public-decision/<int:pk>/assist/', views.assist_form, name='assist_form'),
    path('upvote/<int:assist_id>/', views.upvoteAssist, name='upvote_assist'),
    path('decision/<int:pk>/option/<int:option_id>/filter/', views.filter_option_messages, name='filter_option'),

]