from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomerManager
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


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


class Address(models.Model):
    state = models.CharField()
    city = models.CharField()
    address = models.TextField()
    house_number = models.IntegerField(max_length=4)
    postcode = models.IntegerField(max_length=10)


class Customer(AbstractUser):
    class GenderChoice(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        UNSET = "N", "None"

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GenderChoice.choices, default=GenderChoice.UNSET)
    address = models.ManyToManyField(Address, blank=True)
    email = models.EmailField(_('email address'), unique=True, max_length=30, null=True, blank=True)
    phone = models.CharField(
        max_length=11,
        unique=True,
        null=True, blank=True,
        verbose_name=_('Phone Number'),
        validators=[mobile_number_validation],
        error_messages={
            'unique': _("A user with that Phone number already exists."),
        },
        help_text=_('Example') + " : 09125573688")

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username}"

    objects = CustomerManager()
