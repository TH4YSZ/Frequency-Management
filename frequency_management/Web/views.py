from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User

def homepage(request):
    context= {}
    return render(request, 'homepage.html', context)

def login(request):
    # context = {}
    # dados_senai = Senai.objects.all()
    # context["dados_senai"] = dados_senai

    # if request.method == "POST":
    #     form = FormLogin(request.POST)
    #     if form.is_valid():
    #         var_username = form.cleaned_data['username']
    #         var_password = form.cleaned_data['password']

    #         user = User.objects.create_user(username=var_username, password=var_password)
    #         user.save()
    #         return redirect("cursos")
    #     else:
    #         return redirect("homepage")
    # else:
    #     form = FormLogin()

    # context.update({"form": form})
    return render(request, 'login.html')

def cadastro(request):
    return render(request, 'cadastro.html')

def cursos(request):
    return render(request, 'cursos.html')

def relatorio(request):
    return render(request, 'relatorio.html')

def alunos(request):
    return render(request, 'alunos.html')
