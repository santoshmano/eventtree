from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import SelebUser

class SelebUserCreationForm(UserCreationForm):
    class Meta:
        model = SelebUser
        fields = ("email",)
        error_messages = {
            'email': {
                'unique': _("A user with this email already exists"),
            },
        }
