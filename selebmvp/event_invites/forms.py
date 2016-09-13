from django import forms
from selebmvp.event_invites.models import EventInvite


class RSVPForm(forms.ModelForm):
    class Meta:
        model = EventInvite
        fields = ['full_name', 'email', 'num_of_adults', 'num_of_children',
                  'attending', 'message', 'newsletter', 'invite']
