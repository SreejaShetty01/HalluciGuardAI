from django import forms
from django.contrib.auth.models import User
from authentication.models import UserProfile

class AdminLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Admin Password'})
    )

class UserUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short user biography'})
    )
    gemini_api_key = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gemini API Key'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['bio', 'gemini_api_key']:
                field.widget.attrs['class'] = 'form-control'
        
        if profile:
            self.fields['bio'].initial = profile.bio
            self.fields['gemini_api_key'].initial = profile.gemini_api_key

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.bio = self.cleaned_data.get('bio', '')
            profile.gemini_api_key = self.cleaned_data.get('gemini_api_key', '')
            profile.save()
        return user
