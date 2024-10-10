from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cursos', views.cursos, name='cursos'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('alunos', views.criar_cursos, name='alunos'),
    path('notificacoes', views.notificacoes, name='notificacoes'),
    path('criar_curso', views.criar_cursos, name='criar_curso'),
    path('criar_aluno', views.criar_alunos, name='criar_aluno'),
    path('del_curso', views.delete_curso, name='del_curso'),
    path('logout', views.logout, name='logout')
]   