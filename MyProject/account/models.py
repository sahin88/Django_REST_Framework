from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from rest_framework_simplejwt.tokens import RefreshToken


class MyAccountManager(BaseUserManager):
    def create_user(self,
                    email,
                    username,
                    password=None,
                    is_active=True,
                    is_admin=False,
                    is_superuser=False,
                    is_staff=False,
                    is_verified=False):
        if email is None:
            raise ValueError('User must have an email')
        if username is None:
            raise ValueError('User must have  an Username ')

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)

        user.is_admin = is_admin
        user.is_superuser = is_superuser
        user.is_staff = is_staff
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        username,
        password,
    ):
        user = self.create_user(email=self.normalize_email(email),
                                username=username,
                                password=password,
                                is_active=True,
                                is_admin=True,
                                is_superuser=True,
                                is_staff=True)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, verbose_name='email', unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date_joined',
                                       default=datetime.datetime.now)
    last_login = models.DateTimeField(verbose_name='last_login',
                                      default=datetime.datetime.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'token': str(refresh.access_token)}

    def has_perm(self, perm, obj=None):
        return self.is_admin  #has permissiion if the user is admin

    def has_module_perms(self, app_label):
        return True
