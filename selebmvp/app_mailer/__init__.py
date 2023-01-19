"""This is inspired by https://github.com/django-ses/django-ses.
    But uses boto3
"""

from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

from datetime import datetime, timedelta
from time import sleep

import boto3
import botocore

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# These would be nice to make class-level variables, but the backend is
# re-created for each outgoing email/batch.
# recent_send_times also is not going to work quite right if there are multiple
# email backends with different rate limits returned by SES, but that seems
# like it would be rare.
cached_rate_limits = {}
recent_send_times = []


class AWSSESBackend(BaseEmailBackend):
    """Django Email backend that uses AWS's Simple Email Service (SES).
    """

    def __init__(self, fail_silently=False, aws_access_key=None,
                 aws_secret_key=None, aws_region_name=None,
                 aws_region_endpoint=None, aws_auto_throttle=None,
                 **kwargs):
        """
        Initialize the SES client with passed in Amazon AWS credentials

        Args:
            fail_silently: True if errors are not tobe propogated and ignored.
                These are AWS SES errors
            aws_access_key: Amazon IAM access key.
                (passed only if settings.AWS_ACCESS_KEY is not tobe used)
            aws_secret_key: Amazon IAM Secret.
                (passed only if settings.AWS_SECRET_KEY is not tobe used)
            aws_region_name: Amazon SES Region.
                (passed only if settings.AWS_SES_REGION_NAME is not used)
            aws_auto_throttle: Amazon SES sending rate limit.
                (passed only if settings.AWS_SES_AUTO_THROTTLE is not used)
        """
        super(AWSSESBackend, self).__init__(fail_silently=fail_silently,
                                            **kwargs)
        self._access_key_id = aws_access_key or settings.AWS_ACCESS_KEY
        self._access_key = aws_secret_key or settings.AWS_SECRET_KEY
        self._region = aws_region_name or settings.AWS_SES_REGION_NAME
        self._throttle = aws_auto_throttle or \
            float(settings.AWS_SES_AUTO_THROTTLE)

        try:
            self.client = boto3.client('ses',
                                       aws_access_key_id=self._access_key_id,
                                       aws_secret_access_key=self._access_key,
                                       region_name=self._region,
                                       )
        except:
            if not self.fail_silently:
                raise

    def send_messages(self, email_messages):
        """Sends one or more EmailMessage objects.

        Args:
            email_messages: List of email_messages that needs to be sent.
                The method is called by django's send_email(or send_raw_email)

        Returns:
            Returns the number of email messages sent.
            This is the requirment by django when using a custom Email Backend
        """
        if not email_messages:
            return

        if not self.client:
            # Failed silently
            return

        num_sent = 0
        source = settings.APP_EMAIL_RETURN_PATH
        for message in email_messages:
            # Automatic throttling. Assumes that this is the only SES client
            # currently operating. The AWS_SES_AUTO_THROTTLE setting is a
            # factor to apply to the rate limit, with a default of 0.5 to stay
            # well below the actual SES throttle.
            # Set the setting to 0 or None to disable throttling.
            if self._throttle:
                global recent_send_times

                now = datetime.now()

                # Get and cache the current SES max-per-second rate limit
                # returned by the SES API.
                rate_limit = self.get_rate_limit()

                # Prune from recent_send_times anything more than a few seconds
                # ago. Even though SES reports a maximum per-second, the way
                # they enforce the limit may not be on a one-second window.
                # To be safe, we use a two-second window (but allow 2 times the
                # rate limit) and then also have a default rate limit factor of
                # 0.5 so that we really limit the one-second amount in two
                # seconds.
                window = 2.0  # seconds
                window_start = now - timedelta(seconds=window)
                new_send_times = []
                for time in recent_send_times:
                    if time > window_start:
                        new_send_times.append(time)
                recent_send_times = new_send_times

                # If the number of recent send times in the last 1/_throttle
                # seconds exceeds the rate limit, add a delay.
                # Since I'm not sure how Amazon determines at exactly what
                # point to throttle, better be safe than sorry and let in, say,
                # half of the allowed rate.

                if len(new_send_times) > rate_limit * window * self._throttle:
                    # Sleep the remainder of the window period.
                    delta = now - new_send_times[0]
                    total_seconds = (delta.microseconds + (delta.seconds +
                                     delta.days * 24 * 3600) * 10**6) / 10**6
                    delay = window - total_seconds
                    if delay > 0:
                        sleep(delay)

                recent_send_times.append(now)
                # end of throttling

            try:
                response = self.client.send_raw_email(
                    Source=source or message.from_email,
                    Destinations=message.recipients(),
                    RawMessage={
                        'Data': message.message().as_string()
                    }
                )
                message.extra_headers['status'] = 200
                message.extra_headers['message_id'] = response[
                    'MessageId']
                num_sent += 1
            except botocore.exceptions.ClientError as err:
                # Store failure information so to post process it if required
                error_keys = ['status', 'reason', 'body', 'request_id',
                              'error_code', 'error_message']
                for key in error_keys:
                    message.extra_headers[key] = getattr(err, key, None)
                if not self.fail_silently:
                    raise

        return num_sent

    def get_rate_limit(self):
        """Calculate our own email sending rate limit.

        This is to make sure AWS SES does not reject emails because hit rate
        limit was reached.

        Returns:
            A float representing the internal rate limit
        """
        if self._access_key_id in cached_rate_limits:
            return cached_rate_limits[self._access_key_id]

        if not self.client:
            raise Exception(
                "No connection is available to check current SES rate limit.")

        try:
            quota_dict = self.client.get_send_quota()
            max_per_second = quota_dict['MaxSendRate']
            ret = float(max_per_second)
            cached_rate_limits[self._access_key_id] = ret
            return ret
        finally:
            pass
