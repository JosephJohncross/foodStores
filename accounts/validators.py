import os
from django.core.exceptions import ValidationError

def allowed_image_ext(value):
    print(value)
    file_ext = value.format
    print(file_ext)
    valid_ext_formats = ["png", "jpeg", "jpg", "gif", "webp"]
    if not file_ext.lower() in valid_ext_formats:
        raise ValidationError("Allowed file formats" +  str(valid_ext_formats))