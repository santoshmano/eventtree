from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View

from django.shortcuts import get_object_or_404, redirect, render

from .forms import SelebUserCreationForm

from selebmvp.utils import AppMailer

User = get_user_model()

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def bookings(request):
    context = {
        'packages': request.user.packages
    }
    return render(request, "bookings.html", context)

class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = SelebUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            AppMailer().send_registration_email_to_admin(request.POST.get('email'))
            AppMailer().send_registration_email_to_user(request.POST.get('email'))
            return redirect('/')

        context = {
            'form': form
        }
        return render(request, 'register.html', context)
