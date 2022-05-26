from django.contrib.auth.models import AbstractUser
from django.db import models

from HelpAndDonate.settings import AUTH_USER_MODEL
from donate.managers import UserManager
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    TYPES = (
        (0, 'Fundacja'),
        (1, 'Organizacja pozarządowa'),
        (2, 'Zbiórka lokalna'),
    )
    type = models.IntegerField(choices=TYPES, default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.get_type_display()


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=256, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True,
                             )
