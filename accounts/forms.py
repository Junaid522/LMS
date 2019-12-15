from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
User = get_user_model()
from fractions import Fraction


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'profile_picture', 'password1', 'password2',)

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def clean_username(self):
        username = self.cleaned_data['username']
        username_existed = User.objects.filter(username=username).first()
        if username:
            if username_existed:
                raise forms.ValidationError('Username already exists.')
            else:
                return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['profile_picture'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': "First Name"})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': "Last Name"})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "Username"})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "example@xyz.com", "style": "text-transform: lowercase;"})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control', 'id': 'profile-image'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "Passsword"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Confirm Password"})
        self.fields['password1'].help_text = "Use 8 or more characters with mix of letters, numbers & symbols"
        self.fields['email'].help_text = None


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label= ''
        self.fields['password'].label = ''

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))


class EmailValidationOnForgotPassword(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "example@xyz.com", "style": "text-transform: lowercase;"})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with this email!")

        return email


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', "style": "text-transform: lowercase;"})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', "style": "text-transform: lowercase;"})


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.hidden_pass = password
        if commit:
            self.user.save()
        return self.user