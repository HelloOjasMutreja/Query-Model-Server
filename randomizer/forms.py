from django.forms import ModelForm
from django import forms
from .models import Decision, Category, Option, Assist

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

class TagsInputField(forms.CharField):
    def to_python(self, value):
        # Split input by spaces and strip whitespace
        tags = [tag.strip() for tag in value.split()]

        # Filter out empty tags and enforce character limit
        filtered_tags = []
        for tag in tags:
            if tag and len(tag) <= 45:
                filtered_tags.append(tag)

        # Limit the number of tags to 5
        if len(filtered_tags) > 5:
            filtered_tags = filtered_tags[:5]

        return filtered_tags

    def prepare_value(self, value):
        if value is not None:
            return ' '.join(value)
        return value

class AdditionalFieldsForm(forms.ModelForm):
    # Use the TagsInputField for the 'tags' field
    tags = TagsInputField(label='Tags', required=False)

    class Meta:
        model = Decision
        fields = ['situation', 'contributor_message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['situation'].widget.attrs.update({'rows': '4'})  # Adjust textarea rows if needed
        self.fields['contributor_message'].widget.attrs.update({'rows': '4'})  # Adjust textarea rows if needed

    def clean_tags(self):
        # Validate the 'tags' input, if needed
        tags = self.cleaned_data['tags']
        if not tags:
            raise forms.ValidationError("Please enter at least one tag.")
        return tags

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
