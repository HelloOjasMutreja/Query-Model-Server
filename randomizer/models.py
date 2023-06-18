from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('stopwords')
# Create your models here.

CustomUser = get_user_model()

class Grid(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    data = models.CharField(max_length=36, default='0' * 36)

    def __str__(self):
        return f'Grid for {self.user.username}'

    def generate_data(self):
        num_dots = random.randint(12, 24)
        data = ['1'] * num_dots + ['0'] * (36 - num_dots)
        random.shuffle(data)
        self.data = ''.join(data)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ImageSet(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image_sets/', default='default_image.jpg', null=True)
    color1 = models.CharField(max_length=50, null=True)
    color2 = models.CharField(max_length=50, null=True)
    color3 = models.CharField(max_length=50, null=True)
    color4 = models.CharField(max_length=50, null=True)
    color5 = models.CharField(max_length=50, null=True)
    color6 = models.CharField(max_length=50, null=True)
    color7 = models.CharField(max_length=50, null=True)
    color8 = models.CharField(max_length=50, null=True)
    color9 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)


class Decision(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    is_daily_decision = models.BooleanField(default=False)
    is_quick_decision = models.BooleanField(default=False)
    is_public_decision = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    image_set = models.ForeignKey(ImageSet, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    overview = models.TextField(max_length=500, null=True, blank=True)
    situation = models.TextField(max_length=500, null=True, blank=True)
    contributor_message = models.TextField(max_length=255, null=True, blank=True)
    preference = models.TextField(max_length=400, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Decision instance first

        # Tokenize the title
        words = nltk.word_tokenize(self.title)

        # Get the part-of-speech tags for the words
        pos_tags = pos_tag(words)

        # Filter out unnecessary word types and punctuation marks
        excluded_word_types = ['IN', 'DT', 'PRP$', 'PRP', 'WDT', 'WP', 'WRB', 'VBP', 'VBZ']
        filtered_words = [word.lower() for word, pos in pos_tags if pos not in excluded_word_types and word.isalnum()]

        # Create or retrieve tags
        for word in filtered_words:
            tags = Tag.objects.filter(name=word)
            if tags.exists():
                tag = tags.first()
            else:
                tag = Tag.objects.create(name=word)
            self.tags.add(tag)

    def __str__(self):
        if self.title:
            return self.title.strip()
        return "Untitled Decision"

class Option(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    content = models.TextField(max_length=20)
    is_preferred = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Assist(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    assisted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(max_length=255, null=True, blank=True)
    caution = models.TextField(max_length=255, null=True, blank=True)
    pros = models.TextField(max_length=255, null=True, blank=True)
    cons = models.TextField(max_length=255, null=True, blank=True)
    helpful = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assist by {self.assisted_by.username} on {self.decision.title}"
    
class HelpfulUpvote(models.Model):
    assist = models.ForeignKey(Assist, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Helpful upvote by {self.user.username} on Assist: {self.assist.id}"

class UserDecisionInteraction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    assists = models.IntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    view_time = models.DurationField(null=True, blank=True)
    last_interaction_time = models.DateTimeField(auto_now=True)

    def start_timer(self):
        self.last_interaction_time = timezone.now()
        self.save()

    def stop_timer(self):
        current_time = timezone.now()
        if self.last_interaction_time:
            elapsed_time = current_time - self.last_interaction_time
            self.view_time = self.view_time or timedelta()
            self.view_time += elapsed_time
            self.last_interaction_time = None
            self.save()

    def get_duration(self):
        if self.last_interaction_time:
            current_time = timezone.now()
            elapsed_time = current_time - self.last_interaction_time
            return self.view_time + elapsed_time
        return self.view_time
    
class UserFeedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)
    feedback = models.TextField()

class UserRecommendationRefresh(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_refresh = models.DateTimeField(auto_now=True)