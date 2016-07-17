from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.conf import settings

from .utils import AppMailer

#show the home page
def home(request):
    return render(request, "home.html")

def contact(request):
    if request.is_ajax():
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        sender_email = request.POST.get('email')
        message = request.POST.get('message')

        data = AppMailer().send_contact_us_email_to_admin(
                    name,
                    sender_email,
                    message,
                    phone
                )

        return JsonResponse(data, safe=False)
