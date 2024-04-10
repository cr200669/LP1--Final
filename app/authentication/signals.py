

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=UserProfile)
def user_created(sender, instance, created, **kwargs):
    if created:
        pass
