from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    class GenderChoice(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        UNSET = "N", "None"

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GenderChoice.choices, default=GenderChoice.UNSET)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, max_length=30, blank=True, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "User"

    def __str__(self):
        return f"{self.username}"

    def get_full_name(self):
        # If the full name is not specified, return username
        if self.first_name == "" and self.last_name == "":
            return self.username
        else:
            return self.first_name + " " + self.last_name

    get_full_name.short_description = 'Name'
