from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Decision)
admin.site.register(Option)
admin.site.register(ImageSet)
admin.site.register(Category)
admin.site.register(Assist)
admin.site.register(Tag)
admin.site.register(HelpfulUpvote)
admin.site.register(UserDecisionInteraction)
admin.site.register(Grid)