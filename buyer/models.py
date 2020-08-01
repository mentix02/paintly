from __future__ import annotations

from hashlib import sha256
from datetime import timedelta
from typing import Tuple, Union

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> Buyer:
        if not email:
            raise ValueError('The given email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str = None, **extra_fields) -> Buyer:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> Buyer:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)


class Buyer(AbstractUser):

    username = None
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    email: str = models.EmailField(
        _('email address'), unique=True, help_text='Primary identifier.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def generate_reset_token(self) -> ResetToken:
        return ResetToken.objects.create(
            buyer=self,
            expires_on=timezone.now() + timedelta(days=1),
            token=sha256(
                f'{timezone.now().timestamp()}-{self.username}'.encode()
            ).hexdigest(),
        )

    def set_full_name(self, full_name: str) -> None:
        """
        Django stores the first and last names of a user in separate
        columns so set_full_name simply splits a provided string and
        places the first string before a space as the first_name and
        whatever follows is populated in the last_name field.
        """

        if not full_name:
            return

        full_name = full_name.split()
        self.first_name = full_name[0]

        # Has more than one space.
        if len(full_name) > 1:
            self.last_name = ' '.join(full_name[1:])

        self.save()

    def __str__(self) -> str:
        return self.get_full_name()


class Address(models.Model):

    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=7)
    house_number = models.CharField(max_length=50)
    state = models.CharField(
        max_length=2,
        help_text='Delivery address state.',
        choices=(
            ('AP', 'Andhra Pradesh'),
            ('AR', 'Arunachal Pradesh'),
            ('AS', 'Assam'),
            ('BR', 'Bihar'),
            ('CG', 'Chhattisgarh'),
            ('GA', 'Goa'),
            ('GJ', 'Gujarat'),
            ('HR', 'Haryana'),
            ('HP', 'Himachal Pradesh'),
            ('JK', 'Jammu and Kashmir'),
            ('JH', 'Jharkhand'),
            ('KA', 'Karnataka'),
            ('KL', 'Kerala'),
            ('MP', 'Madhya Pradesh'),
            ('MH', 'Maharashtra'),
            ('MN', 'Manipur'),
            ('ML', 'Meghalaya'),
            ('MZ', 'Mizoram'),
            ('NL', 'Nagaland'),
            ('OR', 'Orissa'),
            ('PB', 'Punjab'),
            ('RJ', 'Rajasthan'),
            ('SK', 'Sikkim'),
            ('TN', 'Tamil Nadu'),
            ('TR', 'Tripura'),
            ('UK', 'Uttarakhand'),
            ('UP', 'Uttar Pradesh'),
            ('WB', 'West Bengal'),
            ('TN', 'Tamil Nadu'),
            ('TR', 'Tripura'),
            ('AN', 'Andaman and Nicobar Islands'),
            ('CH', 'Chandigarh'),
            ('DH', 'Dadra and Nagar Haveli'),
            ('DD', 'Daman and Diu'),
            ('DL', 'Delhi'),
            ('LD', 'Lakshadweep'),
            ('PY', 'Pondicherry'),
        ),
    )

    def __str__(self) -> str:
        return f'{self.house_number} {self.city}, {self.state} {self.pin_code}'


class ResetToken(models.Model):

    token = models.CharField(max_length=64)
    used = models.BooleanField(default=False)
    expires_on = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE, related_name='tokens')

    def __str__(self) -> str:
        return self.token

    def use(self) -> None:
        """
        Makes a ResetToken as used thus rendering it invalid.
        """
        self.used = True
        self.save()

    @classmethod
    def valid_token(
        cls, token: str
    ) -> Union[Tuple[bool, None], Tuple[bool, ResetToken]]:
        try:
            token = cls.objects.get(token__exact=token)
        except ResetToken.DoesNotExist:
            return False, None
        else:
            return token.valid, token

    @property
    def valid(self) -> bool:
        return self.expires_on >= timezone.now() and not self.used
