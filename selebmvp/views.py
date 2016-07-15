from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.conf import settings

import boto3

from django.core.mail import EmailMessage

#show the home page
def home(request):
    return render(request, "home.html")

def contact(request):
    if request.is_ajax():
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        sender_email = request.POST.get('email')
        message = request.POST.get('message')

        msg = EmailMessage(
                'Contact from ' + name,
                message,
                settings.AWS_SES_RETURN_PATH,
                [settings.AWS_SES_RETURN_PATH],
                reply_to=[sender_email])

        data = msg.send()
        return JsonResponse(data, safe=False)
