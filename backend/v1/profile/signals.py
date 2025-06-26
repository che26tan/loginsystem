from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from profile.models import Profile

MyUser = apps.get_model('account', 'MyUser')

@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    """Creates a Profile only when a new MyUsers instance is created."""
    if created:
        print(f"User {instance.username} created. Now creating profile.")
        try:
            # Profile.objects.create(user=instance)
            profile = Profile(user=instance)
            profile.save()
            print(f"Profile created for user {instance.username}.")
        except Exception as e:
            print(f"Error creating profile: {e}")