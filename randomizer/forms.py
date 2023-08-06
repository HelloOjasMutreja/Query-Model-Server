from django.forms import ModelForm
from django import forms
from .models import Decision, Category, Option

class TitleCategoryForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)

class OverviewForm(forms.Form):
    overview = forms.CharField(max_length=500, required=False, widget=forms.Textarea)

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['content']
        widgets = {'content': forms.TextInput(attrs={'placeholder': 'Add option'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = False

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
