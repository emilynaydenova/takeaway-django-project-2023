from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from accounts.managers import CustomUserManager
from accounts.validators import ValidateFileMaxSizeInMb
from Takeaway import settings

from PIL import Image

"""
1. Create model extending User model. -> CustomUser
2. Configure model in settings -> AUTH_USER_MODEL = 'accounts.CustomUser'
3. Create user manager for our model -> managers.py
"""


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    # password comes from AbstractBaseUser
    # last_login comes from AbstractBaseUser

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    # is_superuser comes from PermissionsMixin

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        auto_now_add=True,
        blank=True,
        null=True,
    )
    # groups come from PermissionsMixin
    # user_permissions come from PermissionsMixin

    # says to AbstractBaseUser how to identify the user
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def get_profile(self):
        profile = Profile.objects.filter(pk=self.id)[0]
        return profile

    class Meta:
        verbose_name = "User"


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 25
    LAST_NAME_MAX_LENGTH = 25
    IMAGE_MAX_SIZE_MB = 2
    NO_NAME = "No name"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # make CustomUser.is_active = False
        primary_key=True,  # user and profile will have the same pk
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        blank=True,
        null=True)

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        blank=True,
        null=True)
    # phone = models.CharField(...)
    phone = PhoneNumberField(
        blank=True,
        null=True,
        help_text=_("Contact phone number"))

    image = models.ImageField(
        upload_to="profile_pics",
        blank=True,
        null=True,
        validators=[
            ValidateFileMaxSizeInMb(
                max_size=IMAGE_MAX_SIZE_MB,
            ),
        ],
    )

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        full_name = f'{self.first_name or ""} {self.last_name or ""}'
        if len(full_name.replace(" ", "")) == 0:
            return self.NO_NAME
        elif self.first_name is None:
            return f"{self.last_name}"
        elif self.last_name is None:
            return f"{self.first_name}"
        return full_name

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #     img.thumbnail(output_size)
    #     img.save(self.image)
