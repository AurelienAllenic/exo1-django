from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User

        def create_profile(sender, instance, created, **kwargs):
            if created:
                from .models import Profile
                Profile.objects.create(user=instance)

        post_save.connect(create_profile, sender=User)
