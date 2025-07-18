from django.contrib.auth.base_user import BaseUserManager
import uuid

class UserAccountManager(BaseUserManager):
    def create_user(self, email, REG_no=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')

        if not REG_no:
            # Automatically generate a unique REG_no if not provided
            REG_no = str(uuid.uuid4())[:12]

        email = self.normalize_email(email)
        user = self.model(email=email, REG_no=REG_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Generate REG_no automatically for superusers
        return self.create_user(email=email, REG_no=str(uuid.uuid4())[:12], password=password, **extra_fields)
