from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from api import v1
from api.views import UserViewSet, QuestionViewSet, IJobViewSet

app_name = 'api'
api_v1 = DefaultRouter()
api_v1.register(r'users', UserViewSet)
api_v1.register(r'questions', QuestionViewSet)
api_v1.register(r'jobs', IJobViewSet)

urlpatterns = [
     url(r'v1/', include((api_v1.urls, 'api_v1'), namespace='myapp')),
     url(r'v1/signup/', v1.signup, name='signup'),
]