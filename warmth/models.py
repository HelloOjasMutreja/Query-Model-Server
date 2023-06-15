from django.db import models

# Create your models here.

class Decision(models.Model):
    title = models.CharField(max_length=50)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title