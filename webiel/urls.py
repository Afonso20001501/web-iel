from django.urls import path
from . import views

app_name = 'webiel'

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('noticia/<slug:slug>/', views.NoticiaView.as_view(), name='noticia-view'),# Noticia-View 
    path('sobre/', views.SobreView.as_view(), name="sobre_historial"),# sobre_historial
    path('sobre_missao/', views.SobreMissaoView.as_view(), name="sobre_missao"),# sobre_missão
    path('sobre_estatuto/', views.SobreEstatutoView.as_view(), name="sobre_estatuto"),# sobre_estatuto
    path('sobre_pacto/', views.SobrePactoView.as_view(), name="sobre_pacto"),# sobre_Pacto
    path('sobre_fe/', views.SobreFeView.as_view(), name="sobre_fe"),# sobre_fé
    path('sobre_pratica/', views.SobrePraticaView.as_view(), name="sobre_pratica"),# sobre_pratica
    path('noticia_iel/', views.NoticiaIelView.as_view(), name="noticia_iel"),# Noticia_iel
    path('contato/', views.ContatoView.as_view(), name="contato"),# Contato
    path('mocidade/', views.MocidadeView.as_view(), name="mocidade"),# Mocidade
    path('senhoras/', views.SenhorasView.as_view(), name="senhoras"),# Senhoras
    path('devem/', views.DevemView.as_view(), name="devem"),# Devem
    path('homens/', views.HomensView.as_view(), name="homens"),# Homens
    path('musica/', views.MusicaView.as_view(), name="musica")# Musica
]


