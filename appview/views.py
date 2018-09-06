from django.shortcuts import render
from rest_framework.authtoken.models import Token

def home(request):
    return render(request, 'frontend/home.html',{})

def job(request):
	token = Token.objects.first()
	return render(request, 'jobs/index.html',{"token":token})