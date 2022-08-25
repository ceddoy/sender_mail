import datetime
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.db import models

from authapp.managers import CustomerUserManager
from authapp.validators import AgeMinValueValidator


def date_expired():
    return timezone.now() + datetime.timedelta(days=7)


def generate_token_verify():
    return get_random_string(VerifyCode.CODE_LENGTH)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField('ID', primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_('Email addres'), unique=True)
    age = models.PositiveSmallIntegerField(_('Age'), validators=[AgeMinValueValidator(18)])

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    is_verify = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['age']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


class VerifyCode(models.Model):
    CODE_LENGTH = 10

    token = models.CharField(_('Token Verify'), max_length=CODE_LENGTH, default=generate_token_verify, editable=False)
    data_expired = models.DateTimeField(default=date_expired)
    user = models.OneToOneField('User', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Verify by email'
        verbose_name_plural = 'Verify by emails'

