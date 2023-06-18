from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    profile_pic = forms.ImageField(label='Profile Picture', required=False)
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': 'Date of Birth', 'class': 'form-control'}))
    pseudonymous_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Pseudonymous Name', 'class': 'form-control'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES, required=True)

    def save(self, request):
        user = super().save(request)
        user.profile_pic = self.cleaned_data['profile_pic']
        user.dob = self.cleaned_data['dob']
        user.pseudonymous_name = self.cleaned_data['pseudonymous_name']
        user.gender = self.cleaned_data['gender']
        user.save()
        return user