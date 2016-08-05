"""This module holds all the utils, such as App Emailer
"""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class AppMailer:
    """The class responsible for composing and sending different app emails

    The class uses EmailMultiAlternatives to send raw emails. Both HTML and
    text emails are sent by default.
    The app is set to use Amazon AWS SES as the email backend. Check app_mailer
    app for more details about the custom email backend
    """
    def __init__(self):
        self._from = settings.APP_EMAIL_RETURN_PATH
        self._reply_to = settings.APP_EMAIL_RETURN_PATH

    def send_contact_us_email_to_admin(self, name, email, message, phone=None):
        """send email to admin when someone fills a contact us form.

        Args:
            name: Name in the form
            email: Email in the form
            message: Message in the form
            phone: Phone number in the form (this is optional, defualt to None)
        """
        self._subject = 'You are received a new enquiry from ' + name
        self._to = settings.APP_TO_EMAIL
        self._reply_to = email

        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message
        }

        self._html_message = render_to_string(
                                              'emails/enquiry_admin.html',
                                              context)
        self._text_message = render_to_string(
                                              'emails/enquiry_admin.txt',
                                              context)
        return self.deliver()

    def send_registration_email_to_user(self, email):
        """Send a welcome email to the newly registered user

        Args:
            email: The email of the registered user

        """
        self._subject = 'Welcome to Eventtree'
        self._to = email

        context = {
            'email': email
        }

        self._html_message = render_to_string(
                                              'emails/registration_user.html',
                                              context)
        self._text_message = render_to_string(
                                              'emails/registration_user.txt',
                                              context)
        return self.deliver()

    def send_registration_email_to_admin(self, email):
        """Send a new user registered alert email to admin

        Args:
            email: The email of the registered user
        """
        self._subject = 'A new registration at Eventtree'
        self._to = settings.APP_TO_EMAIL
        self._reply_to = email

        context = {
            'email': email
        }

        self._html_message = render_to_string(
                                              'emails/registration_admin.html',
                                              context)
        self._text_message = render_to_string(
                                              'emails/registration_admin.txt',
                                              context)
        return self.deliver()

    def send_booking_email_to_admin(self, booking, user):
        """Send an email to admin when user decides on a package for a event

        Args:
            booking: Booking object
            user: The SelebUser that selected the booking
        """
        self._subject = 'A user had just confirmed a package'
        self._to = settings.APP_TO_EMAIL
        self._reply_to = user.email

        context = {
            'user': user,
            'booking': booking,
        }

        self._html_message = render_to_string(
                                              'emails/booking.html',
                                              context)
        self._text_message = render_to_string(
                                              'emails/booking.txt',
                                              context)
        return self.deliver()

    def send_test_email(self):
        self._subject = 'This is a test email'
        self._to = settings.APP_TO_EMAIL

        context = {
            'name': 'Sandeep Patil',
            'body': 'This is some test data in the email body'
        }

        self._html_message = render_to_string(
                                              'emails/test_email.html',
                                              context)
        self._text_message = render_to_string(
                                              'emails/test_email.txt',
                                              context)
        return self.deliver()

    def deliver(self):
        """All the send_*_email_* methods will call this method

        Creates a EmailMultiAlternatives object from all the class attributes
        and calls send to send using django core email (which uses AWS SES)
        """
        msg = EmailMultiAlternatives(
                self._subject,
                self._text_message,
                self._from,
                [self._to],
                reply_to=[self._reply_to]
              )

        msg.attach_alternative(self._html_message, "text/html")
        return msg.send()
