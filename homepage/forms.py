from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
User = get_user_model()


class ImageUploadForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('profile_picture',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['profile_picture'].label = ''

        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control', 'id': 'profile-image'})
