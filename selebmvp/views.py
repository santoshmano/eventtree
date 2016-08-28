""" Application level Views"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

from selebmvp.utils import AppMailer


def home(request):
    """Display the home/landing page
    """
    return render(request, "home.html")


def contact(request):
    """Handle the contact us form
    """
    if request.is_ajax():
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        sender_email = request.POST.get('email')
        message = request.POST.get('message')

        data = AppMailer(request).send_contact_us_email_to_admin(
                name,
                sender_email,
                message,
                phone
        )

        return JsonResponse(data, safe=False)


def send_test_email(request):
    AppMailer(request).send_test_email()

    messages.success(request, 'Successfully sent the test email')
    return redirect('home')
