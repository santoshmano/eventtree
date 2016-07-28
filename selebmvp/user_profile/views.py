from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from django.core.exceptions import SuspiciousOperation
from django.utils.decorators import decorator_from_middleware
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render

from selebmvp.user_profile.forms import SelebUserCreationForm
from selebmvp.user_profile.middleware import EventOwnerMiddleware

from selebmvp.utils import AppMailer

from selebmvp.user_packages.models import Event, EventPackage, Booking

#Get custom user model, returns SelebUser
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
    """
    events = request.user.events.all()

    bookings = Booking.objects.filter(status="IP", event__in=events)
    context = {
        'bookings': bookings
    }
    return render(request, "bookings.html", context)

#TODO Combine this and event view to genric views
@login_required
def events(request):
    """Renders the user events page
    """
    context = {
        'packages': request.user.events
    }

    return render(request, "events.html", context)

@login_required
@event_owner
def event(request, slug):
    """Renders the user individual page

    Args:
        slug: The event slug
    """
    event = get_object_or_404(Event, slug=slug)
    context = {
        'event': event
    }
    return render(request, "event_packages.html", context)

@login_required
@event_owner
def select_event(request, slug, package):
    """The view for selecting a package for a given event

    Args:
        slug: The event slug
        package: pk of the selected package
    """

    event = get_object_or_404(Event, slug=slug)
    package = get_object_or_404(EventPackage, pk=package)

    #Check if the given event already has a booking
    if not Booking.objects.filter(event=event).count():
        #raise SuspiciousOperation
        booking = Booking.objects.create(event=event, package=package,
                   slug="-".join(event.name.split() +
                                 package.name.split()))
        messages.success(request, 'You have sussessfully selected a package, \
                                   you will hear from us soon')
        AppMailer().send_booking_email_to_admin(booking, request.user)
    else:
        messages.error(request, 'You have already selected a package for your\
                      event')

    #TODO Check if the package belongs to the event (security check)
    return redirect(events)

#TODO send confirm email link in the registration welcome email
class Register(View):
    """Create new SelebUser

    Creates a new user. Sends an welcome email to clinet and new user registered
    email to admin

    """
    def get(self, request):
        """Show the initial SelebUserCreationForm
        """
        return render(request, 'register.html')

    def post(self, request):
        """Handles the POST SelebUserCreationForm.
        """
        #TODO send emails by handling user_created signal?
        form = SelebUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            AppMailer().send_registration_email_to_admin(request.POST.get('email'))
            AppMailer().send_registration_email_to_user(request.POST.get('email'))
            messages.success(request, 'Your were successfully registered')
            return redirect('/')

        context = {
            'form': form
        }
        return render(request, 'register.html', context)
