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
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view

from api.views import reset_password, oauth2callback
from appview.views import home
from ijobs.views import job

schema_view = get_swagger_view(title='MyApp API')

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('docs/', schema_view),
    url(r'^$', home, name='home'),
    url(r'jobs/', job, name='job'),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                reset_password, name='resetpassword'),
    url(r'^oauth2callback$', oauth2callback, name='oauth2callback'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
