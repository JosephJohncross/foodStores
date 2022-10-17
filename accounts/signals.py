from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserProfile, User

@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance,created ,**kwargs):
    if created:
        UserProfile.objects.create(user = instance)
    else:
        try:
            profile = UserProfile.objects.get(user = instance)
            profile.save()
        except:
            #Create user profile if it doesn't exist
            UserProfile.objects.create(user = instance)
