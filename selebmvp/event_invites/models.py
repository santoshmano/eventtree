from django.db import models
from selebmvp.user_packages.models import Event
import uuid


class Invite(models.Model):
    """Create a new invite when user wants to use the invite feature

    The invite model is created when user clicks on send invite on the events
    details page

    Attributes:
        uuid: the uuid for the invite, tobe used in the url for invite form
        event: the event to which this invite belongs to
    """
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    event = models.OneToOneField(Event, blank=False, null=False,
                                 on_delete=models.CASCADE,
                                 related_name="invite")


class EventInvite(models.Model):
    """Invite List for the selected item.

    The model store list of who is coming and who is not and who is a maybe.
    It saves their name, email and number of attendees.

    Attributes:
        invite: The invite to which the invites belong
        full_name: Full name of the attendee
        email: Email of the attendee
        attending: Enumurated value of Yes, Maybe and No
        num_of_adults: Number of adults attending
        num_of_children: Number of children attending
        message: The message from the attendee to the invitee
        newsletter: Do they want news letter from EventTree
    """

    ATTEND_STATUS = (
        ('YES', 'Yes'),
        ('NO', 'No'),
        ('MAYBE', 'Maybe')
    )

    invite = models.ForeignKey(Invite, blank=False, null=False,
                              on_delete=models.CASCADE,
                              related_name="invites")
    full_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    attending = models.CharField(max_length=5, choices=ATTEND_STATUS,
                              default="YS")
    num_of_adults = models.IntegerField(blank=True, null=True, default=0)
    num_of_children = models.IntegerField(blank=True, null=True, default=0)
    message = models.TextField("Message", blank=True, null=True)
    newsletter = models.BooleanField(default=True)
