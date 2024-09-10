from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cursos', views.cursos, name='cursos'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('alunos', views.alunos, name='alunos'),
]   