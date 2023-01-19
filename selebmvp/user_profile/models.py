"""user_profile modules"""

from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class SelebUserManager(BaseUserManager):
    """Create a custom User model.

    See https://docs.djangoproject.com/en/1.9/topics/\
    auth/customizing/#a-full-example for more details.
    This is just taken from the link
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, password.
        """
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, password.
        """

        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class SelebUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_admin = models.BooleanField(
            _('staff status'),
            default=False,
            help_text=_('Designates whether the user can log \
        into this admin site.'),
    )
    is_active = models.BooleanField(_('Is active?'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = SelebUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin
