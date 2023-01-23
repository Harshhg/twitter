from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(max_length=120)
    email = CIEmailField(unique=True, db_index=True)
    verified_on = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def is_verified(self):
        return bool(self.verified_on)


class EmailToken(models.Model):
    email = CIEmailField(unique=True, db_index=True)
    token = models.CharField(unique=True, max_length=120)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
