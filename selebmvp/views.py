from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
import boto3

#show the home page
def home(request):
    return render(request, "home.html")

def contact(request):
    if request.is_ajax():
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')

        client = boto3.client(
            'ses',
            aws_access_key_id='AKIAJAV7SH7YBX2RN2DA',
            aws_secret_access_key='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',
            region_name='us-west-2',
        )

        response = client.send_email(
            Source='santosh@eventtree.com',
            Destination={
                'ToAddresses': [
                    'santosh@eventtree.com',
                ],
            },
            Message={
                'Subject': {
                    'Data': 'Contact from ' + name,
                },
                'Body': {
                    'Text': {
                        'Data': message,
                    },
                }
            },
            ReplyToAddresses=[
                email,
            ],
        )

        data = {
            'response': response,
        }
        return JsonResponse(data)
