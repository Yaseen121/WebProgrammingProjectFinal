from django import forms
from login.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from django.contrib.auth.hashers import check_password
from django.core.validators import validate_email

#Uses Django's built in forms class. Responsible for setting up the form elements.
#Users our user for the model for the forum
#Adds css through widgets for bootstrap
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

    def clean(self):
        cleaned_data = self.cleaned_data
        username = self.cleaned_data.get('username')
        #Raise an error if username already in use
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError({'username': ['Username already taken']})

        email = self.cleaned_data.get('email')
        #Raise an error if email already in use
        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise forms.ValidationError({'email': ['Email already taken']})

        dob = self.cleaned_data.get('dob')
        #Raise an error if dob empty
        if dob is None:
            raise forms.ValidationError({'dob': ['Invalid date']})

        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

#Uses Django's built in forms class. Responsible for setting up the form elements.
#Adds css through widgets for bootstrap
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

    #valids form by checking if username exists (if it doesnt retursn validation erorr)
    #Then checks if password is correct, if it not r
    def clean(self):
        cleaned_data = self.cleaned_data
        username = self.cleaned_data.get('username')
        member = User.objects.filter(username=username)
        if not member:#If user doesnt exist return username validation error
            raise forms.ValidationError({'username': ['Username not registered']})
        password = self.cleaned_data.get('password')
        user = User.objects.get(username=username)
        password = self.cleaned_data.get('password')
        if not user.check_password(password):#If password not correct return password validation error
            raise forms.ValidationError({'password': ['Wrong password']})

        return cleaned_data
