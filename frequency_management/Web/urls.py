from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cursos', views.cursos, name='cursos'),
    path('alunos/<str:turma>', views.alunos, name='alunos'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('notificacoes', views.notificacoes, name='notificacoes'),
    path('criar_curso', views.criar_cursos, name='criar_curso'),
    path('criar_aluno', views.criar_alunos, name='criar_aluno'),
    path('del_curso/<str:turma>', views.delete_curso, name='del_curso'),
    path('del_aluno/<str:turma>/<str:id_carteirinha>', views.delete_aluno, name='del_aluno'),
    path('logout', views.logout, name='logout'),
    path('freq', views.upload_frequencia, name='freq')
]   