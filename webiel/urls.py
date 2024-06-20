from django.urls import path

from . import views

app_name = 'webiel'

urlpatterns = [
    path('', views.home, name="home"), # Home 
    path('sobre/', views.sobre, name="sobre_historial"),# sobre_historial
    path('sobre_missao/', views.sobre_missao, name="sobre_missao"),# sobre_missão
    path('sobre_estatuto/', views.sobre_estatuto, name="sobre_estatuto"),# sobre_estatuto
    path('sobre_pacto/', views.sobre_pacto, name="sobre_pacto"),# sobre_Pacto
    path('sobre_fe/', views.sobre_fe, name="sobre_fe"),# sobre_fé
    path('sobre_pratica/', views.sobre_pratica, name="sobre_pratica"),# sobre_pratica
    path('noticia_iel/', views.noticia_iel, name="noticia_iel"),# Noticia_iel
    path('contato/',  views.contato, name="contato"),# Contato
    path('mocidade/',  views.mocidade, name="mocidade"),# Mocidade
    path('senhoras/',  views.senhoras, name="senhoras"),# Senhoras
    path('devem/',  views.devem, name="devem"),# Devem
    path('homens/',  views.homens, name="homens"),# Homens
    path('musica/',  views.musica, name="musica")# Musica
]


