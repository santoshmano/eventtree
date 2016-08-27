"""user_profile app views
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import decorator_from_middleware
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import datetime
from django.conf import settings
from django.db.models import Sum

import stripe

from selebmvp.user_profile.forms import SelebUserCreationForm
from selebmvp.user_profile.middleware import EventOwnerMiddleware
from selebmvp.utils import AppMailer
from selebmvp.user_packages.models import (Event, EventPackage, Booking,
                                           Payments)
from selebmvp.event_invites.models import Invite
from selebmvp.event_invites.forms import RSVPForm

# Stripe API key
stripe.api_key = settings.STRIPE_SEC_KEY

# Get custom user model, returns SelebUser
User = get_user_model()

# A decorator used to check the if the requesting user is asking for his owner
# events
event_owner = decorator_from_middleware(EventOwnerMiddleware)


@login_required
def dashboard(request):
    """Renders the user dashboard
    """
    return render(request, "dashboard.html")


@login_required
def bookings(request):
    """Renders the user bookings page

    Args:
        request: HttpRequest

    Returns:
        object: HttpResponse
    """
    events = request.user.events.all()

    bookings = Booking.objects.filter(status="IP", event__in=events)
    completed_bookings = Booking.objects.filter(status="CP", event__in=events)
    context = {
        'bookings': bookings,
        'completed_bookings': completed_bookings,
        'stripe_pvt_key': settings.STRIPE_PVT_KEY
    }

    return render(request, "bookings.html", context)


# TODO Combine this and event view to genric views
@login_required
def show_events(request):
    """Renders the user events page

    Args:
        request: HttpRequest

    Returns:
        object:  HttpResponse
    """
    context = {
        'packages': request.user.events
    }

    return render(request, "events.html", context)


@login_required
@event_owner
def show_event(request, slug):
    """Renders the user individual page

    Args:
        slug: The event slug

    Returns:
        object: HttpResponse
    """
    event = get_object_or_404(Event, slug=slug)
    context = {
        'event': event
    }
    try:
        if event.invite:
            num_attending =\
                event.invite.invites.filter(attending="YES").aggregate(
                    Sum('num_of_adults'), Sum('num_of_children'))

            num_maybe =\
                event.invite.invites.filter(attending="MAYBE").aggregate(
                    Sum('num_of_adults'), Sum('num_of_children'))

            num_not_attending =\
                event.invite.invites.filter(attending="NO").count()
                
            context.update({
                'num_adults_attending': num_attending['num_of_adults__sum'],
                'num_children_attending': num_attending['num_of_children__sum'],
                'num_adults_maybe': num_maybe['num_of_adults__sum'],
                'num_children_maybe': num_maybe['num_of_children__sum'],
                'num_not_attending': num_not_attending
            })
    except:
        pass

    return render(request, "event_packages.html", context)


@login_required
@event_owner
def select_event(request, slug, package):
    """The view for selecting a package for a given event

    Args:
        slug: The event slug
        package: pk of the selected package

    Returns:
        object: HttpResponseRedirect
    """

    event = get_object_or_404(Event, slug=slug)
    package = get_object_or_404(EventPackage, pk=package)

    # Check if the given event already has a booking
    if not Booking.objects.filter(event=event).count():
        # raise SuspiciousOperation
        booking = Booking.objects.create(event=event, package=package,
                                         slug="-".join(event.name.split() +
                                                       package.name.split()))
        messages.success(request, 'You have sussessfully selected a package, \
                                   you will hear from us soon')
        AppMailer(request).send_booking_email_to_admin(booking, request.user)
    else:
        messages.error(request, 'You have already selected a package for your\
                      event')

    # TODO Check if the package belongs to the event (security check)
    return redirect(show_events)

@login_required
@event_owner
def charge(request, slug, b_id):
    """The view for accepting credit card charges

    Args:
        request: HttpRequest
        slug: Event SLug
        b_id: Booking id
    """

    booking = Booking.objects.filter(slug=b_id).first()

    try:
        response = stripe.Charge.create(
          amount=int(booking.amount) * 100,
          currency="usd",
          source=request.POST.get('stripeToken'),
          metadata={'order_id': b_id}
        )

        data = response.to_dict()

        Payments.objects.create(booking=booking,
                                stripe_payment_id=data['id'],
                                amount=data['amount'],
                                response=str(data),
                                payment_date=datetime.datetime.fromtimestamp(
                                    int(data['created'])))

        booking.status = "CP"
        booking.payment_date = datetime.datetime.fromtimestamp(
                                int(data['created']))
        booking.save()

        messages.success(request,
                         'Payment Successful')

    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        # body = e.json_body
        # err = body['error']

        messages.error(request,
                       'There were errors with your payment, please try again')
        # print ("Status is: %s" % e.http_status
        # print "Type is: %s" % err['type']
        # print "Code is: %s" % err['code']
        # # param is '' in this case
        # print "Param is: %s" % err['param']
        # print "Message is: %s" % err['message']
        # except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        pass
    # except stripe.error.InvalidRequestError as e:
    #     # Invalid parameters were supplied to Stripe's API
    #     pass
    # except stripe.error.AuthenticationError as e:
    #     # Authentication with Stripe's API failed
    #     # (maybe you changed API keys recently)
    #     pass
    # except stripe.error.APIConnectionError as e:
    #     # Network communication with Stripe failed
    #     pass
    # except stripe.error.StripeError as e:
    #     # Display a very generic error to the user, and maybe send
    #     # yourself an email
    #     pass
    # except Exception as e:
    #     # Something else happened, completely unrelated to Stripe
    #     pass

    return redirect('user_bookings')

@login_required
@event_owner
def send_invite(request, slug):
    """The view for sending an invite to the event to the event owner

        Args:
            slug: The event slug

        Returns:
            object: HttpResponseRedirect
        """

    event = get_object_or_404(Event, slug=slug)

    if event.can_invite():
        # Check if the given event already has a invite
        if not Invite.objects.filter(event=event).count():
            Invite.objects.create(event=event)

        AppMailer(request).send_invite_email_to_event_owner(event,
                                                            request.user)

        messages.success(request,
                     'Your invite email has been successfully sent')
    else:
        messages.error(request,
                       'Sorry, you cannot send an invite at this stage')

    # TODO Check if the package belongs to the event (security check)
    return redirect(show_event, slug=event.slug)


class EventRSVP(View):
    """Handles the get and post for event rsvp
    """
    def get(self, request, uuid):
        """Show the initial SelebUserCreationForm

        Args:
            request: HttpRequest

        Returns:
            object: HttpResponse
        """
        invite = get_object_or_404(Invite, uuid=uuid)
        context = {
            'invite': invite
        }
        return render(request, 'rsvp_form.html', context)

    def post(self, request, uuid):
        """Handles the POST SelebUserCreationForm.

        Args:
            request: HttpRequest

        Returns:
            object: HttpResponse
        """
        invite = get_object_or_404(Invite, uuid=uuid)
        form = RSVPForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for RSVP')
            return redirect('/')

        context = {
            'form': form,
            'invite': invite
        }
        return render(request, 'rsvp_form.html', context)

# TODO send confirm email link in the registration welcome email
class Register(View):
    """Create new SelebUser

    Creates a new user. Sends an welcome email to clinet and new user
    registered email to admin

    """
    def get(self, request):
        """Show the initial SelebUserCreationForm

        Args:
            request: HttpRequest

        Returns:
            object: HttpResponse
        """
        return render(request, 'register.html')

    def post(self, request):
        """Handles the POST SelebUserCreationForm.

        Args:
            request: HttpRequest

        Returns:
            object: HttpResponse
        """
        # TODO send emails by handling user_created signal?
        form = SelebUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            AppMailer(request).send_registration_email_to_admin(
                                                    request.POST.get('email'))
            AppMailer(request).send_registration_email_to_user(
                                                    request.POST.get('email'))
            messages.success(request, 'Your were successfully registered')
            return redirect('/')

        context = {
            'form': form
        }
        return render(request, 'register.html', context)
