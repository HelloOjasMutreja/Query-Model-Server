from django.db.models import Count, Sum, Q
from .models import Decision, UserDecisionInteraction
import random
from datetime import timedelta
from django.utils import timezone
from .models import Decision, UserDecisionInteraction, UserRecommendationRefresh

def get_user_preferred_tags(user):
    interactions = UserDecisionInteraction.objects.filter(user=user)
    tag_counts = interactions.values('decision__tags__name').annotate(
        frequency=Count('decision__tags__name'),
        total_assists=Sum('assists'),
        total_click_count=Sum('click_count'),
        total_view_time=Sum('view_time')
    ).order_by('-frequency', '-total_assists', '-total_click_count', '-total_view_time')
    preferred_tags = [tag_count['decision__tags__name'] for tag_count in tag_counts]
    return preferred_tags
# end def

def get_recommendations(user, num_recommendations=15):
    # Check if 20 minutes have passed since the last refresh
    refresh_interval = timedelta(minutes=1)
    now = timezone.now()
    try:
        last_refresh = UserRecommendationRefresh.objects.get(user=user).last_refresh
        if now - last_refresh < refresh_interval:
            # Less than 20 minutes have passed since the last refresh, so don't generate new recommendations
            return []
    except UserRecommendationRefresh.DoesNotExist:
        # This is the first time generating recommendations for this user, so create a new UserRecommendationRefresh object
        UserRecommendationRefresh.objects.create(user=user)
    
    # Update the timestamp of the last refresh
    UserRecommendationRefresh.objects.filter(user=user).update(last_refresh=now)
    
    preferred_tags = get_user_preferred_tags(user)
    assisted_decisions = UserDecisionInteraction.objects.filter(user=user, assists__gt=0).values_list('decision', flat=True)
    
    # Get recommended decisions
    recommended_decisions = Decision.objects.filter(
        tags__name__in=preferred_tags
    ).exclude(
        id__in=assisted_decisions
    ).exclude(
        Q(title='') | Q(title=None) | Q(title='Untitled decision')
    ).annotate(
        total_assists=Sum('userdecisioninteraction__assists'),
        total_click_count=Sum('userdecisioninteraction__click_count'),
        total_view_time=Sum('userdecisioninteraction__view_time')
    ).order_by('-total_assists', '-total_click_count', '-total_view_time')
    
    # Calculate the number of recommended and non-recommended decisions to include
    num_recommended = int(num_recommendations * 0.6)
    num_non_recommended = num_recommendations - num_recommended
    
    # Get non-recommended decisions
    non_recommended_decisions = Decision.objects.exclude(id__in=recommended_decisions.values_list('id', flat=True)).order_by('?')[:num_non_recommended]
    
    # Combine the recommended and non-recommended decisions
    decisions = list(recommended_decisions[:num_recommended]) + list(non_recommended_decisions)
    
    # Shuffle the list of decisions
    random.shuffle(decisions)
    
    return decisions
# end def