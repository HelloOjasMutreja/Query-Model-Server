from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from randomizer.models import Decision, Assist, HelpfulUpvote, Grid
from .models import CustomUser
from django.db.models import Count
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_grid(sender, instance, created, **kwargs):
    if created:

        grid = Grid.objects.create(user=instance)
        grid.generate_data()
        grid.save()

def userProfile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    content_type = ContentType.objects.get_for_model(user)
    recent_activity = LogEntry.objects.filter(content_type=content_type, object_id=user.id).order_by('-action_time')[:10]
    recent_decisions = Decision.objects.filter(user=user).order_by('-updated', '-created')[:5]
    recent_assists = Assist.objects.filter(assisted_by=user).order_by('-created')[:5]
    upvoted_assists = user.upvoted_assists.all()
    upvote_count = Assist.objects.filter(assisted_by=user).aggregate(total_upvotes=Count('helpfulupvote')).get('total_upvotes', 0)

    tab = request.GET.get('tab', 'decisions')  # Default to 'decisions'
    
    # Fetch data based on the selected tab
    if tab == 'decisions':
        data = recent_decisions
    elif tab == 'assists':
        data = recent_assists
    elif tab == 'saved':
        data = upvoted_assists

    try:
        grid = Grid.objects.get(user=user)
        context = {
            'user': user,
            'recent_activity': recent_activity,
            'recent_decisions': recent_decisions,
            'recent_assists': recent_assists,
            'upvoted_assists': upvoted_assists,
            'upvote_count': upvote_count,
            'grid': grid,
            'data': data,
            'selected_tab': tab,
        }
    except Grid.DoesNotExist:
        context = {
            'user': user,
            'recent_activity': recent_activity,
            'recent_decisions': recent_decisions,
            'recent_assists': recent_assists,
            'upvoted_assists': upvoted_assists,
            'upvote_count': upvote_count,
            'data': data,
            'selected_tab': tab,
        }

    return render(request, 'accounts/user_profile.html', context)
#  end def

@login_required
def editUser(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.save()
        return redirect(userProfile)
    
    return render(request, 'accounts/edit_user.html')