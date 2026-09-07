from django import forms
from django.contrib.auth.forms import UserCreationForm


from .models import User

class SignupForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email already exists')
        return email

    def save(self, commit = True):
        user: User = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    """For users editing their own profile info (not password)"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A user with that email already exists. ')
        return email

class LoginForm(forms.Form):
    """
    Plain Form, not ModelForm — login isn't creating/editing a model instance,
    just validating credentials against one.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



















