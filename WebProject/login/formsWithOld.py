from django import forms
from login.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm

####This one assumes you're trying to create a new user as it uses forms.ModelForm
class LoginFormOld(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            "username": forms.TextInput(
                attrs={
                    'class': 'form-username form-control',
                    'name': 'username',
                    'placeholder': 'Username...',
                }),
            "password": forms.PasswordInput(
                attrs={
                    'class': 'form-password form-control',
                    'name': 'password',
                    'placeholder': 'Password...',
                }),
        }
        labels = {
            'username': "",
            'password': "",
        }
        help_texts = {
            'username': ""
        }

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'gender', 'dob', 'hobby', 'image']
        widgets = {
            "username": forms.TextInput(
                attrs={
                    'class': 'form-username form-control',
                    'name': 'username',
                    'placeholder': 'Username...',
                 }),
            "password": forms.PasswordInput(
                attrs={
                    'class': 'form-password form-control',
                    'name': 'password',
                    'placeholder': 'Password...',
                 }),
            "email": forms.TextInput(
                attrs={
                    'class': 'form-email form-control',
                    'name': 'email',
                    'placeholder': 'E-Mail...',
                 }),
            "gender": forms.Select(
                attrs={
                    'class': 'form-control',
                    'name': 'gender',
                    'placeholder': 'Gender..',
                 }),
            "dob": forms.TextInput(
                attrs={
                    'placeholder': 'Date of Birth:',
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'date',
                    'name': 'dob',
                    'onfocus': "(this.placeholder='', this.type='date')",
                    'onblur': "if(this.value==''){this.placeholder='Date of Birth...', this.type='text'}",
                 }),
            "hobby": forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'id': 'hobby',
                    'name': 'hobby',
                 }),
            "image": forms.FileInput(
                attrs={
                    'type': 'file',
                    'class': 'form-control',
                    'id': 'image',
                    'name': 'image',
                    'accept': 'image/*',
                 }),
        }
        labels = {
            'username': "",
            'password': "",
            'email': "",
            'gender': "",
            'dob': "",
            'hobby': "What hobbies are you interested in?",
            'image': "",
        }
        help_texts = {
            'username': ""
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-username form-control',
            'name': 'username',
            'placeholder': 'Username...'
         }
    ))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-password form-control',
            'name': 'password',
            'placeholder': 'Password...'
         }
    ))

class filterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'class': 'form-username form-control',
            'name': 'username',
            'placeholder': 'Username...'
         }
    ))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={
            'class': 'form-password form-control',
            'name': 'password',
            'placeholder': 'Password...'
         }
    ))
