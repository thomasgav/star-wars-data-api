import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'surname']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}: {self.surname} {self.name}"
