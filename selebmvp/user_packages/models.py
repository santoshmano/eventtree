from django.db import models

from selebmvp.user_profile.models import SelebUser

class UserPackages(models.Model):
    filename = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(SelebUser, blank=True, null=True, related_name="packages")
