from django.shortcuts import render, redirect
from django.urls import reverse


def homepage(request):
    context= {}
    return render(request, 'homepage.html', context)

def login(request):
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def cursos(request):
    return render(request, 'cursos.html')

def relatorio(request):
    return render(request, 'relatorio.html')
