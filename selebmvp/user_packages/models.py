""" All the models for the user_packages modules"""
from django.db import models

from selebmvp.user_profile.models import SelebUser


class Event(models.Model):
    """Event model represents an event

    Every Eventtree event will have one event.

    Attributes:
        name: Name of the event
        slug: A automatically generated slug to be used in urls. Unique.
            This must be used everywhere in the public websites for cross ref
        date: Date on which event is held
        owners: A foreign key to User table.
            There can be more than one owner (who can manage the event)
    """
    name = models.CharField("event name",
                            max_length=250,
                            help_text="Enter the Event Name",)
    slug = models.SlugField("event slug",
                            help_text="-nated Event Name",
                            unique=True)
    date = models.DateField(null=True, blank=True,)
    image = models.CharField("event image",
                             max_length=250,
                             help_text="Enter the Image Filename",
                             null=True,
                             blank=True,)
    owners = models.ManyToManyField(SelebUser,
                                    verbose_name="who can manage this event",
                                    related_name="events")
    send_invite = models.BooleanField("Can Send Invite", default=False)

    # prepopulated_fields = {"slug": ("name",)}

    def event_owners(self):
        """Return a ',' seperated values of event owners first_name.
            If first_name is not set, email is used
        """
        return ", ".join([
            owner.first_name or owner.email
            for owner in self.owners.all()
        ])

    def __str__(self):
        return self.slug

    def can_invite(self):
        """Decides if the user can send invites
        """
        return self.send_invite


class EventPackage(models.Model):
    """List of packages that is sent to the client to select.

    A event can have more than 1 packages to choose from. Eact package will
    have a package details file designed manually at first, look at filename
    attribrute for details

    Attributes:
        filename: The name of the file in user_profile/templates/packages
            folder that will be rendered as the tab content of the individual
            packages (details of the package)
        name: The name of the package for easy identification, user as
            tab name as well
        event: The event to which this belongs, note that this is not a
            one-to-one relation. <TODO> Make it a one-to-one relation
    """
    filename = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

    # <TODO> make this a one-to-one relation
    event = models.ForeignKey(Event, blank=True, null=True,
                              related_name="packages")

    def __str__(self):
        return self.name


class Booking(models.Model):
    """The Booking model that a confirmed booking(s) for a event.

    The moment Client selects a package for a event, a Booking is created
    with a status "CR". Once Admin confirms the price, the status is changed to
    "IP". Once Client make a payment, the status changes to "CP"

    <TODO>There can be more than 1 booking for a event, this is temporary,
    so that clients can be given a way to make any additional payments
    if needed.

    Attributes:
        BOOKING_STATUS: A tuple of tuple that is source for choices
            for the status attribute
        slug: A automatically generated slug to be used in urls. Unique.
            This must be used everywhere in the public websites for cross ref
        event: Event to which this booking belongs
        package: The selected package
        summary: A brief about the selected package and the event
        filename: The name of the file in user_profile/templates/bookings
            folder that will be rendered as the final package details.
            What all services were selected, etc.
        amount: The total price chargable to the Client for the Event
        status: The various state the Booking can be in.
            Refer to class description above and BOOKING_STATUS attribute
        payment_date: Date and time when the payment was confirmed
    """
    BOOKING_STATUS = (
        ('CR', 'Created'),
        ('IP', 'In Progress'),
        ('CP', 'Completed')
    )

    slug = models.SlugField("booking slug",
                            max_length=255,
                            help_text="-nated Name for referring to this\
                            booking",
                            unique=True)
    event = models.ForeignKey(Event, blank=False, null=False,
                              on_delete=models.CASCADE,
                              related_name="booking")
    package = models.ForeignKey(EventPackage, blank=False, null=False,
                                on_delete=models.CASCADE,
                                related_name="booking")
    summary = models.TextField("Summary of the booking",)
    filename = models.CharField(max_length=150)
    amount = models.FloatField("Event cost", default=0.00)
    status = models.CharField(max_length=2, choices=BOOKING_STATUS,
                              default="CR")
    payment_date = models.DateTimeField("Stripe payment date",
                                        null=True,
                                        blank=True)

    # prepopulated_fields = {"slug": ("event", "package",)}


class Payments(models.Model):
    """Store details about stripe payments received

    Attributes:
        booking: Booking id, ForeignKey to Booking
        stripe_payment_id: payment id from stripe
        amount: payment amount
        response: complete JSON response from stripe
        payment_date: payment date returned from stripe
    """

    booking = models.ForeignKey(Booking, blank=False, null=False,
                                related_name="payments")
    stripe_payment_id = models.CharField("stripe payment id",
                                         max_length=150)
    amount = models.FloatField("amount")
    response = models.TextField("json response")
    payment_date = models.DateTimeField("payment date")
