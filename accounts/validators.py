import os
from django.core.exceptions import ValidationError

def allowed_image_ext(value):
    file_ext = os.path.splitext(value.name)[1]
    valid_ext_formats = [".png", ".jpeg", ".jpg", '.gif']
    if not file_ext.lower() in valid_ext_formats:
        raise ValidationError("Allowed file formats" +  str(valid_ext_formats))