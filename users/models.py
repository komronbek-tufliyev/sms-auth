from django.db import models
from .managers import UserManager
# Create your models here.
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    _USER_ERROR_MESSAGE = 'Bunday foydalanuvchi topilmadi'

    username = None
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^998[0-9]{2}[0-9]{7}$', message='Faqat o\'zbek raqamlari tasdiqlanadi')
    phone = models.CharField(_('Telefon raqami'), validators=[phone_regex], max_length=17, unique=True)
    eskiz_id = models.CharField(max_length=20, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    eskiz_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD: str = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def isVerified(self):
        return self.is_verified

class SMSClient(models.Model):
    name = models.CharField()
    phone = models.CharField()