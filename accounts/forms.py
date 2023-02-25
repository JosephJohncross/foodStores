from django import forms
from django.forms import EmailInput, NumberInput, PasswordInput, TextInput
from .models import User,UserProfile    
from .validators import allowed_image_ext
from cloudinary.forms import CloudinaryFileField

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
                'class': 'bg-gray-50 border-b border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder' : 'john.doe@company.com'
            }),
            'username': TextInput(attrs={
                'class': "bg-gray-50 border-b border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
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
            raise forms.ValidationError(
                "Password does not match!"
            )
        if terms_and_condition:
            pass
        else:
            raise forms.ValidationError(
                "Please accept terms and and condition"
            )


class UserProfileForm(forms.ModelForm):
    profile_picture = CloudinaryFileField(options={ 'folder': 'users/profile_pictures'}, widget=forms.FileInput(attrs={'class': "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), validators=[allowed_image_ext], required=False)
    cover_photo = CloudinaryFileField(options={ 'folder': 'users/cover_photos'}, widget=forms.FileInput(attrs={'class': "font-monserat block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), validators=[allowed_image_ext],  required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'id':"home-search",'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)
    country = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)
    state = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)
    pin_code = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}),  required=False)
    latitude = forms.CharField(widget=forms.TextInput(attrs={'id':"lat",'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400", "readonly": "readonly"}), required=False)
    longitude = forms.CharField(widget=forms.TextInput(attrs={'id':"long",'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400", "readonly": "readonly"}), required=False)
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

class UserFormInfo(forms.ModelForm):
    """Based on the User model. Represents the form for the user profile"""
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
