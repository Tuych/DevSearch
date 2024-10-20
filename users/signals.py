from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )


def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def update_user(sender, instance, created, **kwargs):
    profile = instance    # profile bu instansedagi class yani pastda post saveda sender=Profile classiga teng
    user = profile.user   #Profiedagu user BU User clasi bilan bog'langan column

    if created is False:        # agar profile yangi qushilmasa bu degani uzgartirilsa
        user.first_name = profile.name      # Profile clasida firs_name uzgarsa User clasida ham avtamatik ravishda uzgaradi
        user.username = profile.username
        user.email = profile.email
        user.save()


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=Profile)
post_save.connect(update_user, sender=Profile)
