import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import *
from django.utils import timezone
from datetime import timedelta
from home.models import Department, Batch, University

def generate_custom_id():
    # Generate a UUID4 and take first 10+ characters (you can adjust logic here)
    return uuid.uuid4().hex[:50]

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        default=generate_custom_id
    )
    name = models.CharField(max_length=500, default='User')
    email = models.EmailField(unique=True, max_length=500)
    REG_no = models.CharField(unique=True, max_length=50, default=generate_custom_id)

    university = models.ForeignKey(University, on_delete=models.SET_NULL , null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Batch or Session')

    is_active = models.BooleanField(default=True)
    is_CR = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='useraccount_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='useraccount_permissions',
        blank=True
    )

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Only email is required for superuser

    def __str__(self):
        return self.email
