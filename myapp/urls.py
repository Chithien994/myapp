"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from api.views import home, oauth2callback
from appview.views import home, jobs

schema_view = get_swagger_view(title='MyApp API')

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('docs/', schema_view),
    url(r'^$', home, name='home'),
    url(r'jobs/', job, name='job')
    url(r'^oauth2callback$', oauth2callback, name='oauth2callback'),
]
