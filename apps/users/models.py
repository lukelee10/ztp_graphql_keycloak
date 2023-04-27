from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.data_tables.models import AccessAttribute, Classification


class User(AbstractUser):
    clearance = models.ForeignKey(Classification, on_delete=models.PROTECT, null=True, blank=True)
    access_attributes = models.ManyToManyField(AccessAttribute, blank=True)
