import json

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import csrf_exempt

from api.serializers import NewUserSerializer
from core.utils import validate_user_data
from core.enums import ValidationStatusCode
from core.constants import VALIDATION_CODE

User = get_user_model()

@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.AllowAny,))
def signup(request):
    print(request.data)
    """
    Signup new user
    """
    email = request.data.get('email')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')
    full_name = request.data.get('full_name')
    code, message = validate_user_data(request.data)
    if code and message:
        return HttpResponse(json.dumps({'code': code, 'message': message}),
                            content_type='application/json',
                            status=200)
    if User.objects.filter(email=email).exists():
        return HttpResponse(json.dumps({'code': 400, 'message': _('This email already exists in our system')}),
                            content_type='application/json',
                            status=200)
    if not User.objects.filter(phone_number=phone_number).exists():
        user = User.objects.create_user(
            email, full_name, phone_number, password)
        return HttpResponse(json.dumps(NewUserSerializer(user).data),
                            content_type='application/json',
                            status=200)
    return HttpResponse(json.dumps({'code': 400, 'message': _('This phone number already exists in our system')}),
                        content_type='application/json',
                        status=200)


@api_view(['POST'])
@csrf_exempt
@permission_classes((permissions.AllowAny,))
def login(request):
    """
    Login
    """
    phone_number = request.data.get('phone_number')
    if User.objects.filter(phone_number=phone_number).exists():
        password = request.data.get('password')
        user = User.objects.get(phone_number=phone_number)
        if user.check_password(password):
            return HttpResponse(json.dumps(NewUserSerializer(user).data),
                                content_type='application/json',
                                status=200)
        else:
            return HttpResponse(json.dumps({'code': ValidationStatusCode.PASSWORD_IS_INVALID.value, 'message': VALIDATION_CODE[ValidationStatusCode.PASSWORD_IS_INVALID]}),
                                content_type='application/json',
                                status=200)
    else:
        return HttpResponse(json.dumps({'code': ValidationStatusCode.PHONE_NUMBER_IS_INVALID.value, 'message': VALIDATION_CODE[ValidationStatusCode.PHONE_NUMBER_IS_INVALID]}),
                            content_type='application/json',
                            status=200)