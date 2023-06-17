from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile


# reciever is a function
# key word arguments  **kwargs
# post_save signal
# sender is the user

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
            print('Only created user profile')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
# post_save.connect(post_save_create_profile_receiver, sender=User)