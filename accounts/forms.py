from pyexpat import model
from django import forms
from django.forms import EmailInput, NumberInput, PasswordInput, TextInput
from .models import User

class UserForm(forms.ModelForm):
    terms_and_condition = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={
            'class': "w-4 h-4 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-blue-600 dark:ring-offset-gray-800"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
            'placeholder' : '***********'
        }
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
         attrs={
            'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        }
    ))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                'placeholder' : 'John'
            }),
            'last_name': TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder' : 'John'
            }),
            'email': EmailInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder' : 'john.doe@company.com'
            }),
            'username': TextInput(attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                'placeholder' : 'John'
            }),
            'password': PasswordInput(attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                'placeholder' : '***********'
            }),
        }
        error_messages = {
            'first_name': {
                'required': "Please enter your first name"
            },
            'last_name': {
                'required': "Please enter your last name"
            },
            'email': {
                'required': "email is required",
                'unique': 'Email already exist'
            },
            'username': {
                'required': "Username is required",
                "unique": "Username already exist"
            }
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        terms_and_condition = cleaned_data.get('terms_and_condition')

        if password != confirm_password:
            print('password does not match')
            raise forms.ValidationError(
                "Password does not match!"
            )
        if terms_and_condition:
            pass
        else:
            raise forms.ValidationError(
                "Please accept terms and and condition"
            )