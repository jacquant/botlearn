from django.db import models


class SandboxProfile(models.Model):
    profile_name = models.CharField(max_length=60)
    image_name = models.CharField(max_length=60)
    image_id = models.CharField(max_length=60, blank=True, null=True)
    dockerfile = models.FileField(blank=True, null=True)
