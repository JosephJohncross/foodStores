from django import forms
from .models import Category, FoodItem
from accounts.validators import allowed_image_ext
from cloudinary.forms import CloudinaryFileField

class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':"block px-4 py-5 w-full text-sm text-gray-900 resize-none bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400", 'required': 'False'}))
    
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class FoodItemForm(forms.ModelForm):
    food_title = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':"block px-4 py-5 w-full text-sm text-gray-900 resize-none bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400", 'required': 'False'}))
    price = forms.CharField(widget=forms.TextInput(attrs={'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}))
    image = CloudinaryFileField(options={ 'folder': 'foodimages'}, widget=forms.FileInput(attrs={'class': "block w-full text-sm text-gray-400 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400", "placeholder": "image"}), validators=[allowed_image_ext])

    class Meta:
        model = FoodItem
        fields = ['food_title', 'description', 'price', 'image', 'is_available']