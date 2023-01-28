from django import forms
from accounts.validators import allowed_image_ext

from vendor.models import Vendor, OpeningHour

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': "font-monserat block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}), validators=[allowed_image_ext])
    vendor_name = forms.CharField(widget=forms.TextInput(attrs={'id': "floating_outlined", 'class':"block px-4 py-3 w-full text-sm text-gray-900 bg-transparent rounded-lg border-1 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"}))

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
        

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["day", "from_hour", "to_hour", "is_closed"]