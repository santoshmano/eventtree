"""Admin related classes"""
from django.contrib import admin
from .models import Event, EventPackage, Booking


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Event Admin
    """
    fieldsets = [
        ("Events", {"fields": ["name", "image", "slug", "date",
                               "owners", "send_invite"]})
    ]

    def event_owners(self, obj):
        """Reutrn list of event owners
        """
        return obj.event_owners()

    list_display = ("name", "date", "event_owners",)


@admin.register(EventPackage)
class EventPackageAdmin(admin.ModelAdmin):
    """Event Package Admin
    """
    fieldsets = [
        ("Event Packages", {"fields": ["filename", "name", "event"]}),
    ]

    list_display = ("filename", "name", "event",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Booking Admin
    """
    fieldsets = [
        ("Bookings", {"fields": ["event", "package", "summary", "filename",
                                 "slug", "amount", "status", "payment_date"]}),
    ]

    list_display = ("event", "package", "amount", "status", "payment_date",)
