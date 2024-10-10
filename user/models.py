from django.db import models

# Create your models here.


class BasicUser(models.Model):
    step1 = models.JSONField(default=dict, blank=True)
    step2 = models.JSONField(default=dict, blank=True)
