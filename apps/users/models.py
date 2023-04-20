from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.documents.models import Classification


class User(AbstractUser):
    clearance = models.ForeignKey(Classification, on_delete=models.PROTECT, null=True, blank=True)
