from django.forms import ModelForm
from django import forms
from .models import Decision, Category, Assist

class DecisionForm(ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Decision
        fields = '__all__'
        exclude = ['user', 'is_daily_decision', 'image_set']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['categories'].initial = kwargs['instance'].categories.all()
