from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def update_last_updated(sender, instance, **kwargs):
    # Ensure the save was not triggered by the signal
    if not kwargs.get('created', False):
        if instance.pk and not hasattr(instance, '_saving'):
            instance._saving = True
            instance.modified_at = timezone.now()
            instance.save(update_fields=['modified_at'])
