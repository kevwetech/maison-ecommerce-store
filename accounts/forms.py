from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser

# Signup Form

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email



# Login Form

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )



# Update Info Form

class UserUpdateInfoForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }



# Change Password Form

class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})
    )



    