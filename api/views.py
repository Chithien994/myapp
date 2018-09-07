# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.urls import reverse

from rest_framework.decorators import permission_classes
from rest_framework import exceptions, viewsets, permissions
from rest_framework.authentication import BasicAuthentication, \
    SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from core.utils import get_site_url
from api.serializers import UserSerializer, QuestionSerializer, IJobSerializer
from polls.models import Question
from ijobs.models import IJob

User = get_user_model()

class CustomTokenAuthentication(TokenAuthentication):
    model = Token

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication,
                              SessionAuthentication, BasicAuthentication]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication,
                              SessionAuthentication, BasicAuthentication]

class IJobViewSet(viewsets.ModelViewSet):
    queryset = IJob.objects.all()
    serializer_class = IJobSerializer

@csrf_exempt
@permission_classes((permissions.IsAuthenticated,))
def oauth2callback(request):
    from oauth2client import client
    if not request.user.is_superuser:
        return redirect(reverse('home'))
    scopes = [
        'https://www.googleapis.com/auth/androidpublisher'
    ]
    flow = client.flow_from_clientsecrets(
        settings.CLIENT_SECRET,
        scope=','.join(scopes),
        redirect_uri=get_site_url() + reverse('oauth2callback'))
    flow.params['include_granted_scopes'] = 'true'
    flow.params['approval_prompt'] = 'force'
    flow.params['access_type'] = 'offline'
    try:
        auth_uri = flow.step1_get_authorize_url()
        if request.GET.get('code'):
            auth_code = request.GET.get('code')
            credentials = flow.step2_exchange(auth_code)
            with open(settings.CLIENT_DATA, 'w') as f:
                print('credentials', credentials.to_json())
                f.write(credentials.to_json())
            return redirect(reverse('home'))
        return redirect(auth_uri)
    except:
        return redirect(reverse('home'))