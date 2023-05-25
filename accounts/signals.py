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
      #  it will create user profile as soon as user is created
       UserProfile.objects.create(user=instance)
       print('user profie is created')
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except: 
            UserProfile.objects.create(user=instance)
            print('profile was not exist, but I created one')

@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'this user is being saved')


# post_save.connect(post_save_create_profile_receiver, sender=User)