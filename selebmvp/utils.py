from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class AppMailer:
    def __init__(self):
        self._from = settings.AWS_SES_RETURN_PATH
        self._reply_to = settings.AWS_SES_RETURN_PATH

    def send_contact_us_email_to_admin(self, name, email, message, phone=None):
        self._subject = 'You are received a new enquiry from ' + name
        self._to = settings.AWS_SES_TO_EMAIL
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
        self._subject = 'A new registration at Eventtree'
        self._to = settings.AWS_SES_TO_EMAIL
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

    def deliver(self):
        msg = EmailMultiAlternatives(
                self._subject,
                self._text_message,
                self._from,
                [self._to],
                reply_to=[self._reply_to]
              )

        msg.attach_alternative(self._html_message, "text/html")
        return msg.send()
