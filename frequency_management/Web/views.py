from django.shortcuts import render, redirect
from django.urls import reverse


def homepage(request):
    context= {}
    return render(request, 'homepage.html', context)

def login(request):
    return render(request, 'login.html')