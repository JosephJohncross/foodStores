from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserProfile, User

@receiver(post_save, sender=User)
def post_save_create_profile_reciever(sender, instance,created ,**kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user = instance)
        print('user profile is created')
    else:
        try:
            profile = UserProfile.objects.get(user = instance)
            profile.save()
            print("Profile was not present but is updated")
        except:
            #Create user profile if i doesn't exist
            UserProfile.objects.create(user = instance)
            print("Profile does not exist, create a new one")
        print("user is updated")

