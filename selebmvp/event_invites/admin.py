from django.contrib import admin
from selebmvp.event_invites.models import Invite, EventInvite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Invites", {"fields": ["event"]}),
    ]

    def event_name(self, obj):
        return obj.event

    def num_of_rsvps(self, obj):
        return obj.invites.count()

    list_display = ("event_name", "num_of_rsvps",)


@admin.register(EventInvite)
class EventInviteAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Event Invitees", {"fields": ["invite", "full_name", "email",
                                       "attending", "num_of_adults",
                                       "num_of_children", "newsletter"]}),
    ]

    def event_name(self, obj):
        return obj.invite

    list_display = ("event_name", "full_name", "email", "attending", "newsletter",)