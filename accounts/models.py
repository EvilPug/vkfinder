from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.contrib.postgres.fields import *


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vk_id = models.IntegerField(unique=True, null=True)
    vk_token = models.CharField(max_length=128, unique=True, null=True)
    city_title = models.CharField(max_length=32, blank=True, null=True)
    photo_200_orig = models.TextField(max_length=32, blank=True)

    group_list = ArrayField(models.IntegerField(), blank=True, null=True)
    favorite_users = ArrayField(models.IntegerField(), blank=True, null=True)
    badges = ArrayField(models.CharField(max_length=16), blank=True, null=True)


class Badge(models.Model):

    code = models.CharField(max_length=16, unique=True)
    title = models.CharField(max_length=16, blank=True)
    description = models.TextField(null=True, blank=True)
    src = models.CharField(max_length=16, blank=True)
    can_get = models.BooleanField(blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
