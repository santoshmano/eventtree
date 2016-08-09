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
from selebmvp.views import home, contact, send_test_email
from selebmvp.user_profile.views import (Register, bookings, events,
                                         event, select_event, charge,)
from django.contrib.auth import views
from django.contrib.auth.decorators import user_passes_test

# login_forbidden = user_passes_test(lambda u: u.is_anonymous(),
# lazy(reverse, str)('my-url-name'))
login_forbidden = user_passes_test(
                    lambda u: u.is_anonymous(), '/user/bookings/')

urlpatterns = [

    # Auth
    url(r'^login/$', login_forbidden(views.login),
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/'}, name='logout'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^password_reset/$', views.password_reset,
        {'template_name': 'password_reset.html',
         'email_template_name': 'emails/password_reset_request.txt',
         'html_email_template_name': 'emails/password_reset_request.html'},
        name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done,
        {'template_name': 'password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/\
        (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        {'template_name': 'password_reset_form.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),

    # Admin
    url(r'^admin/', admin.site.urls),

    # Application
    # The home url '/'. displays landing page
    url(r'^$', home, name='home'),
    url(r'^contact/', contact, name='contact'),

    # User
    # url(r'^user/dashboard/', dashboard, name='user_dashboard'),

    # TODO #
    # PRODUCTION_MODE_CHECK #
    # comment the below this once email template testing is done
    # should be commendted in production mode/before going live
    url(r'^sendtestemail/$', send_test_email, name='send_test_email'),

    url(r'^user/bookings/$', bookings, name='user_bookings'),
    url(r'^user/events/$', events, name='user_events'),
    url(r'^user/events/(?P<slug>[\w-]+)/$', event, name='user_event'),
    url(r'^user/events/select/(?P<slug>[\w-]+)/(?P<package>[-\w]+)/$',
        select_event, name='user_select_event'),
    url(r'^user/stripe/charge/(?P<slug>[\w-]+)/(?P<b_id>[-\w]+)/$',
        charge, name='user_stripe_charge'),
]
