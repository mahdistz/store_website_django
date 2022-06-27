from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class MobileNumberValidator(RegexValidator):
    # A rejection to check user input information
    regex = r"^[0][9]\d{9}$"

    message = _(
        'Enter a valid mobile number. This value may contain only numbers.'
    )
    flags = 0


# create an instance from the class
mobile_number_validation = MobileNumberValidator()


class User(AbstractUser):
    class GenderChoice(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        UNSET = "N", "None"

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GenderChoice.choices, default=GenderChoice.UNSET)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11,
                             unique=True,
                             validators=[mobile_number_validation],
                             error_messages={
                                 'unique': _("A user with that Phone number already exists."),
                             }
                             , blank=True)
    email = models.EmailField(_('email address'), unique=True, max_length=30, blank=True, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = CustomUserManager

    class Meta:
        verbose_name_plural = "User"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"

    def get_full_name(self):
        # If the full name is not specified, return username
        if self.first_name == "" and self.last_name == "":
            return self.username
        else:
            return self.first_name + " " + self.last_name

    get_full_name.short_description = 'Name'
