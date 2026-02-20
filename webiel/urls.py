from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('adolescentes/', views.AdolescentesView.as_view(), name="adolescentes"),# Mocidade
    path('senhoras/', views.SenhorasView.as_view(), name="senhoras"),# Senhoras
    path('devem/', views.DevemView.as_view(), name="devem"),# Devem
    path('homens/', views.HomensView.as_view(), name="homens"),# Homens
    path('musica/', views.MusicaView.as_view(), name="musica"),# Musica
    path('registro/', views.RegistrationView.as_view(), name="registro"),# Registro
    path('inscricao/create/', views.inscricao_create, name='inscricao_create'),
    path('api/precos-atividades/', views.get_precos_atividades, name='precos_atividades'),
    path('api/atividades/', views.lista_atividades, name='lista_atividades'),
    path('consultar-inscricao/<str:referencia>/', views.consultar_inscricao, name='consultar_inscricao'),
    path('pagar-prestacao/<str:referencia>/', views.pagar_prestacao, name='pagar_prestacao'),
    path('inscricao/search/', views.search_inscricao, name='search_inscricao'),  # Novo endpoint para busca
    path('inscricao/pay_second/', views.pay_second_inscricao, name='pay_second_inscricao'),  # Novo endpoint para pagamento da segunda prestação
   
    
    #AREA DE ADMINISTRAÇÃO
    path('login/', auth_views.LoginView.as_view(
        template_name='webiel/pages/login.html',
        redirect_authenticated_user=True,
        next_page='webiel:dashboard'
    ), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='webiel/pages/password_reset.html'
    ), name='password_reset'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),   
    path('marcar-feita/', views.marcar_feita, name='marcar_feita'),
    path('cartas-feitas/', views.CartasFeitasView.as_view(), name='cartas_feitas'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='webiel/pages/password_reset.html'), name='password_reset'),
    path('publicacoes/criar/', views.CriarPublicacaoView.as_view(), name='publicacao_criar'),
    path('publicacoes/editar/<slug:slug>/', views.EditarPublicacaoView.as_view(), name='publicacao_editar'),
    path('publicacoes/deletar/<slug:slug>/', views.DeletarPublicacaoView.as_view(), name='publicacao_deletar'),
    path('nubentes/', views.NubentesListView.as_view(), name='nubentes'),
    path('nubentes/download/', views.DownloadNubentesView.as_view(), name='nubentes_download'),
    path('publicacoes/', views.PublicacoesListView.as_view(), name='publicacoes'),
    path('publicacoes/toggle/', views.toggle_publicacao, name='toggle_publicacao'),
    path('banco-de-alimentacao/', views.BancoDeAlimentacaoListView.as_view(), name='banco_de_alimentacao'),
    path('banco-de-alimentacao/download/', views.DownloadBancoDeAlimentacaoView.as_view(), name='banco_de_alimentacao_download'),
    path('marcar-feita/', views.marcar_feita, name='marcar_feita'),
    path('visualizar-carta/<int:carta_id>/', views.visualizar_carta, name='visualizar_carta'),
    path('editar-carta/<int:carta_id>/', views.editar_carta, name='editar_carta'),
    path('deletar-carta/<int:carta_id>/', views.deletar_carta, name='deletar_carta'),

    path('nubentes/detalhes/', views.nubente_detalhes, name='nubente_detalhes'),
    path('nubentes/editar/', views.nubente_editar, name='nubente_editar'),
    path('nubentes/deletar/', views.nubente_deletar, name='nubente_deletar'),
    path('fotos/criar/', views.CriarFotoView.as_view(), name='criar_foto'),

     # Nova URL para mensagens e newsletter
    path('mensagens-newsletter/', views.MensagensNewsletterView.as_view(), name='mensagens_newsletter'),
    path('mensagem/editar/<int:pk>/', views.EditarMensagemView.as_view(), name='editar_mensagem'),
    path('mensagem/deletar/<int:pk>/', views.DeletarMensagemView.as_view(), name='deletar_mensagem'),
    path('newsletter/editar/<int:pk>/', views.EditarNewsletterView.as_view(), name='editar_newsletter'),
    path('newsletter/deletar/<int:pk>/', views.DeletarNewsletterView.as_view(), name='deletar_newsletter'),


    path('cartas-recebidas/', views.CartasRecebidasView.as_view(), name='cartas_recebidas'),
    path('carta-detalhes/', views.carta_detalhes, name='carta_detalhes'),
    path('carta-editar/', views.carta_editar, name='carta_editar'),
    path('carta-deletar/', views.carta_deletar, name='carta_deletar'),

    path('inscricoes/', views.InscricoesView.as_view(), name='inscricoes'),
    path('inscricao-detalhes/', views.inscricao_detalhes, name='inscricao_detalhes'),
    path('inscricao-editar/', views.inscricao_editar, name='inscricao_editar'),
    path('inscricao-deletar/', views.inscricao_deletar, name='inscricao_deletar'),
    path('download-inscricoes-pdf/', views.download_inscricoes_pdf, name='download_inscricoes_pdf'),
  
]


