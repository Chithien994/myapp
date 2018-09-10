from django.shortcuts import render
from rest_framework.authtoken.models import Token

def job(request):
	token = Token.objects.first()
	return render(request, 'ijobs/index.html',{"token":token})
