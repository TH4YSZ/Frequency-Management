from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login', views.login, name='login'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('cursos', views.cursos, name='cursos'),
    path('relatorio', views.relatorio, name='relatorio'),
    path('alunos', views.alunos, name='alunos'),
    path('notificacoes', views.notificacoes, name='notificacoes'),
    path('delete_curso/int:id>', views.delete_curso, name="del_curso"),
    path('logout', views.logout, name='logout')
]   