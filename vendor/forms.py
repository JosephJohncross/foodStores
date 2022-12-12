from django import forms
from django.forms import TextInput

from vendor.models import Vendor

class VendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': "font-monserat block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}))
    vendor_name = forms.CharField(widget=forms.TextInput(attrs={'id': "floating_outlined", 'class':"block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"}))

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        # widgets = {
        #     'vendor_name': TextInput(attrs={
        #         'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
        #         'placeholder' : 'The chills'
        #     })
        # }
