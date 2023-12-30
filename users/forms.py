# Django
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import Profile

# Utils
import re

class SignupForm(forms.Form):
    # Signup Form
    username = forms.CharField(label=False, min_length=4, max_length=50, widget = forms.TextInput(attrs={'placeholder':'Username','class': 'form-control', 'onkeyup': 'without_space(this);'}))
    password = forms.CharField(label=False, max_length=70, widget = forms.PasswordInput(attrs={'placeholder':'Password','class': 'form-control'}))
    password_confirmation = forms.CharField(label=False, max_length=70, widget = forms.PasswordInput(attrs={'placeholder':'Password confirmation','class': 'form-control'}))
    email = forms.CharField(label=False, min_length=6, max_length=70, widget = forms.EmailInput(attrs={'placeholder':'Email','class': 'form-control'}))

    def clean_username(self):
        # Username must be unique
        username = self.cleaned_data["username"]
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError("Username is already in use")
        return username

    def clean(self):
        # Verify password confirmation match
        data = super().clean()

        password = data["password"]
        password_confirmation = data["password_confirmation"]

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long and include at least one digit and one uppercase letter.")

        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must be at least 8 characters long and include at least one digit and one uppercase letter.")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must be at least 8 characters long and include at least one digit and one uppercase letter.")

        return data

    def save(self):
        # Create user and profile
        data = self.cleaned_data
        data.pop("password_confirmation")

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()