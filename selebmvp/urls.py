"""selebmvp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import home, contact
from selebmvp.user_profile.views import dashboard, Register, bookings
from django.contrib.auth import views

urlpatterns = [

    #Auth
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),

    #Admin
    url(r'^admin/', admin.site.urls),

    #Application
    # The home url '/'. displays landing page
    url(r'^$', home, name='home'),
    url(r'^contact/', contact, name='contact'),

    #User
    #url(r'^user/dashboard/', dashboard, name='user_dashboard'),
    url(r'^user/bookings/', bookings, name='user_bookings'),
]
