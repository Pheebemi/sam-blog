from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CryptoUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg bg-dark-100 border border-dark-200 text-white focus:outline-none focus:border-secondary transition-colors',
            'placeholder': 'Enter your email'
        })
    )

    class Meta:
        model = CryptoUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style username field
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg bg-dark-100 border border-dark-200 text-white focus:outline-none focus:border-secondary transition-colors',
            'placeholder': 'Enter your username'
        })
        # Style password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg bg-dark-100 border border-dark-200 text-white focus:outline-none focus:border-secondary transition-colors',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg bg-dark-100 border border-dark-200 text-white focus:outline-none focus:border-secondary transition-colors',
            'placeholder': 'Confirm your password'
        })

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-3 rounded-lg bg-dark-100 border border-dark-200 text-white focus:outline-none focus:border-secondary transition-colors'
            })