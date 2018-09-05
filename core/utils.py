#coding: utf-8
import datetime
import re
from datetime import timedelta

import httplib2
import oauth2client
from apiclient import discovery
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import get_template
from rest_framework.views import exception_handler

from core.constants import VALIDATION_CODE
from core.enums import ValidationStatusCode
from django.core.mail import EmailMultiAlternatives


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None and 'code' in response.data:
        status_code = ValidationStatusCode(int(response.data['code']))
        response.data['message'] = VALIDATION_CODE[status_code]

    return response


def is_email(string):
    from django.core.exceptions import ValidationError
    from django.core.validators import EmailValidator

    validator = EmailValidator()
    try:
        validator(string)
    except ValidationError:
        return False
    return True


def validate_user_data(data):
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')
    full_name = data.get('full_name')
    code, message = None, None
    if not phone_number:
        code = ValidationStatusCode.PHONE_NUMBER_IS_INVALID.value
        message = VALIDATION_CODE[ValidationStatusCode.PHONE_NUMBER_IS_INVALID]
    elif not password:
        code = ValidationStatusCode.PASSWORD_IS_INVALID.value
        message = VALIDATION_CODE[ValidationStatusCode.PASSWORD_IS_INVALID]
    elif not email:
        code = ValidationStatusCode.EMAIL_ADDRESS_IS_EMPTY.value
        message = VALIDATION_CODE[ValidationStatusCode.EMAIL_ADDRESS_IS_EMPTY]
    elif email and not is_email(email):
        code = ValidationStatusCode.EMAIL_ADDRESS_IS_INVALID.value
        message = VALIDATION_CODE[ValidationStatusCode.EMAIL_ADDRESS_IS_INVALID]
    elif not full_name:
        code = ValidationStatusCode.FULL_NAME_IS_EMPTY.value
        message = VALIDATION_CODE[ValidationStatusCode.FULL_NAME_IS_EMPTY]
    return code, message


def send_email(subject, message_html, email_from, email_to, obj_model):
    if not message_html:
        raise ValueError(
            ("Either message_plain or message_html should be not None"))

    if not email_from:
        email_from = settings.DEFAULT_FROM_EMAIL

    """ initial data using bind value to html template """
    data = {'obj': obj_model}
    if message_html:
        html_content = get_template(message_html).render(data)

    message = {}
    message['subject'] = subject
    message['body'] = html_content
    message['from_email'] = email_from
    message['to'] = email_to
    msg = EmailMultiAlternatives(**message)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def get_site_url():
    current_site = Site.objects.get_current()
    if settings.PRODUCTION:
        SITE_URL = 'https://' + current_site.domain
    else:
        SITE_URL = 'http://' + current_site.domain
    return SITE_URL


def get_credentials():
    store = oauth2client.file.Storage(settings.CLIENT_DATA)
    credentials = store.get()
    refresh_mins = settings.REFRESH_MINS
    if (credentials.token_expiry - datetime.datetime.utcnow()) < timedelta(minutes=refresh_mins):
        credentials.refresh(httplib2.Http())
    return credentials


def verify_purchased(packageName, productId, token):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('androidpublisher', 'v3', http=http)
    r = service.purchases().products().get(
        packageName=packageName, productId=productId, token=token)
    result = r.execute()
    return result

def is_mobile(request):
    """Return True if the request comes from a mobile device."""
    if not hasattr(request, 'META'):
        return False
    MOBILE_AGENT_RE = re.compile(r".*(iphone|ipad|tablet|mobile|android|touch)",re.IGNORECASE)
    print('HTTP_USER_AGENT', request.META.get('HTTP_USER_AGENT', ''))
    if MOBILE_AGENT_RE.match(request.META.get('HTTP_USER_AGENT', '')):
        return True
    else:
        return False