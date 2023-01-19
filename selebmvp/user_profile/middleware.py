"""Contains all the Custom Middlewares
"""
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from selebmvp.user_packages.models import Event


class EventOwnerMiddleware:
    """This is a custom middleware to check for event ownership.

    This is used as a decorator for the views that deals with event display
    and modification. It checks if the event requested is owned by the
    requesting user.

    See https://docs.djangoproject.com/en/1.9/ref/utils/#django.utils
    .decorators.decorator_from_middleware and
    https://docs.djangoproject.com/en/1.9/topics/http/middleware/#writing
    -your-own-middleware

    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        # return HttpResponse("".join(view_kwargs['slug']),
        #         content_type="application/json", status=403)
        event = get_object_or_404(Event, slug=view_kwargs['slug'])
        if event not in request.user.events.all():
            raise PermissionDenied
        else:
            return None
