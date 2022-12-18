from django.shortcuts import render
from django.http import HttpResponse

def settings(request):
    return HttpResponse('settings')
