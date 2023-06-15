from django.forms import ModelForm
from .models import Decision


class DecisionForm(ModelForm):
    class Meta:
        model = Decision
        fields = '__all__'