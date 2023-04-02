from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    UserChangeForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
# from django.contrib.auth.models import User

'''Все классы форм должны быть в forms.py'''

from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'feild-reg', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'feild-reg', 'placeholder': 'Пароль'}))
    class Meta:
        model = CustomUser
        fields = ('name', 'last_name', 'email', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'class':'feild-reg', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'feild-reg', 'placeholder': 'Фамилия'}),
            'phone': forms.TextInput(attrs={'class': 'feild-reg', 'placeholder': 'Телефон'}),
            'email': forms.EmailInput(attrs={'class': 'feild-reg', 'placeholder': 'e-mail'}),
            'password1': forms.PasswordInput(attrs={'class': 'feild-reg', 'placeholder': 'Пароль'}),
            'password2': forms.PasswordInput(attrs={'class': 'feild-reg', 'placeholder': 'Повторите пароль'}),
            }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('name', 'last_name', 'email', 'phone')


class LoginUserForm(AuthenticationForm, forms.Form):
    username = forms.CharField(label='email', widget=forms.EmailInput(attrs={'class': 'feild-reg', 'id': 'username', 'placeholder': 'email'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'feild-reg', 'id': 'password', 'placeholder': 'Пароль'}))

class ResetPasswordUserForm(PasswordResetForm, forms.Form):

    email = forms.CharField(label='email', widget=forms.EmailInput(attrs={
        'class': 'feild-reg', 'placeholder': 'email'}))

class MySetPasswordForm(SetPasswordForm, forms.Form):

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'feild-reg', 'placeholder': 'Пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'feild-reg', 'placeholder': 'Повторите пароль'}))

    error_messages = {
    'password_mismatch': ("The two password fields didn't match."),
    }




