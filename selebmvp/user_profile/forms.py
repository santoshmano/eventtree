from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from selebmvp.user_profile.models import SelebUser


class SelebUserCreationForm(UserCreationForm):
    """A custome user creation form based from UserCreationForm

    Added to generate a custom error message for the email field of SelebUser
    """

    class Meta:
        model = SelebUser
        fields = ("email",)
        error_messages = {
            'email': {
                'unique': _("A user with this email already exists"),
            },
        }
