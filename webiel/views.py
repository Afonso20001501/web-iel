from datetime import timedelta, timezone, datetime
import logging
from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView, CreateView,  View
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Atividade, BancoDeAlimentacao, Carta, CartaRecebida, Casamento, Category, Department, Devem, Homens, Inscricao, Mensagem, Mocidade, Musica, Newsletter, Noticia, Photo, Prestacao, Senhoras
from .forms import BancoForm, CasaForm, CartForm, MensForm, NewsForm, NoticiaForm, PhotoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from django.db.models import Sum
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from webiel import models
from io import BytesIO
import decimal
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.core.validators import FileExtensionValidator

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from io import BytesIO
from datetime import date, datetime
from .models import Inscricao, Atividade, Department
import logging



class Home(TemplateView):     
    template_name = 'webiel/pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        noticias = Noticia.objects.filter(is_published=True).order_by('-id')
        paginator = Paginator(noticias, 3)
        noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'noticias': noticias,
            'noticias_recentes': noticias_recentes,
            'banco_form': BancoForm(),
            'casa_form': CasaForm(),
            'carta_form': CartForm(),
            'news_form': NewsForm(),
            'page_obj': page_obj, 
        })
        
        return context
      
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        casa_form = CasaForm(request.POST)
        carta_form = CartForm(request.POST)
        news_form = NewsForm(request.POST)

        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif casa_form.is_valid():
            messages.success(request, 'A sua inscrição foi feita com sucesso!', extra_tags='casa')
            casa_form.save()
        elif carta_form.is_valid():
            messages.success(request, 'A sua solicitação enviada com sucesso!', extra_tags='carta')
            carta_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Subescrição feita com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao salvar o formulário. Por favor, verifique os dados e tente novamente.')
        
        return self.get(request, *args, **kwargs)

class NoticiaView(DetailView):
    model = Noticia
    template_name = 'webiel/pages/noticia-view.html'
    context_object_name = 'noticia' 

    def get_object(self, queryset=None):
        return get_object_or_404(Noticia, slug=self.kwargs.get('slug'), is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)

        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class SobreView(TemplateView):
    template_name = 'webiel/pages/sobre_historial.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class SobreMissaoView(TemplateView):
    template_name = 'webiel/pages/sobre_missao.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class SobreEstatutoView(TemplateView):
    template_name = 'webiel/pages/sobre_estatuto.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class SobrePactoView(TemplateView):
    template_name = 'webiel/pages/sobre_pacto.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class SobreFeView(TemplateView):
    template_name = 'webiel/pages/sobre_fe.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class SobrePraticaView(TemplateView):
    template_name = 'webiel/pages/sobre_pratica.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class NoticiaIelView(TemplateView):
    template_name = 'webiel/pages/noticia_iel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        noticias = Noticia.objects.filter(is_published=True).order_by('-id')
        paginator = Paginator(noticias, 6)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        context['noticias'] = noticias
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        context['page_obj'] = page_obj
        
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class ContatoView(TemplateView):
    template_name = 'webiel/pages/contato.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['mens_form'] = MensForm()
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        mens_form = MensForm(request.POST)
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if mens_form.is_valid():
            messages.success(request, 'A sua mensagem foi enviada com sucesso!', extra_tags='contact')
            mens_form.save()
        elif banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class MocidadeView(TemplateView):
    template_name = 'webiel/pages/mocidade.html'
    department_slug = 'mocidade'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['atividade_mocidades'] = Mocidade.objects.filter().order_by('-id')
        context['department'] = get_object_or_404(Department, slug=self.department_slug)
        context['photos'] = Photo.objects.filter(department=context['department']).order_by('-upload_date')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)

class AdolescentesView(TemplateView):
    template_name = 'webiel/pages/adolescentes.html'
    department_slug = 'adolescentes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['atividade_adolescente'] = Mocidade.objects.filter().order_by('-id')
        context['department'] = get_object_or_404(Department, slug=self.department_slug)
        context['photos'] = Photo.objects.filter(department=context['department']).order_by('-upload_date')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)
    
class SenhorasView(TemplateView):
    template_name = 'webiel/pages/senhoras.html'
    department_slug = 'sociedade-de-senhoras'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['atividade_senhoras'] = Senhoras.objects.filter().order_by('-id')
        context['department'] = get_object_or_404(Department, slug=self.department_slug)
        context['photos'] = Photo.objects.filter(department=context['department']).order_by('-upload_date')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class DevemView(TemplateView):
    template_name = 'webiel/pages/devem.html'
    department_slug = 'demd'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['atividade_devems'] = Devem.objects.filter().order_by('-id')
        context['department'] = get_object_or_404(Department, slug=self.department_slug)
        context['photos'] = Photo.objects.filter(department=context['department']).order_by('-upload_date')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class HomensView(TemplateView):
    template_name = 'webiel/pages/homens.html'
    department_slug = 'sociedade-de-homens'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['atividade_homens'] = Homens.objects.filter().order_by('-id')
        context['department'] = get_object_or_404(Department, slug=self.department_slug)
        context['photos'] = Photo.objects.filter(department=context['department']).order_by('-upload_date')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)
    
class MusicaView(TemplateView):
    template_name = 'webiel/pages/musica.html'
    department_slug = 'musica'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-id')
        context['atividade_musicas'] = Musica.objects.filter().order_by('-id')
        context['department'] = get_object_or_404(Department, slug=self.department_slug)
        context['photos'] = Photo.objects.filter(department=context['department']).order_by('-upload_date')
        context['banco_form'] = BancoForm()
        context['news_form'] = NewsForm()
        return context
    
    def post(self, request, *args, **kwargs):
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
        
        if banco_form.is_valid():
            messages.success(request, 'O seu donativo foi enviado com sucesso!', extra_tags='banco')
            banco_form.save()
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')

        return self.get(request, *args, **kwargs)

class DepartmentView(TemplateView):
    template_name = None  # Definido por cada departamento
    department_slug = None  # Definido por cada departamento

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obter departamento
        department = Department.objects.get(slug=self.department_slug)
        context['department'] = department

        # Obter fotos com paginação
        photos = Photo.objects.filter(department=department).order_by('-upload_date')
        paginator = Paginator(photos, 12)  # 12 fotos por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['photos'] = page_obj.object_list

        # Contexto existente (atividades, notícias, etc.)
        context['atividade_adolescentes'] = []  # Substitua pela query de atividades
        context['noticias_recentes'] = Noticia.objects.filter(is_published=True).order_by('-created_at')[:4]
        return context
    
class RegistrationView(TemplateView):
    template_name = 'webiel/pages/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departamentos'] = Department.objects.all()
        return context

@require_POST
@ensure_csrf_cookie
def inscricao_create(request):
    if request.method != 'POST':
        logger.error("Método HTTP inválido")
        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=400)

    try:
        # Verificação de requisição AJAX
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.error("Requisição não é AJAX")
            return JsonResponse({'success': False, 'error': 'Requisição inválida'}, status=400)

        # Carrega e valida os dados do formulário
        try:
            form_data = json.loads(request.POST.get('formData', '{}'))
            logger.info(f"Dados recebidos: {form_data}")
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Formato de dados inválido'}, status=400)

        # Validação dos dados obrigatórios
        campos_obrigatorios = ['activity', 'departamento', 'fullName', 'email', 'phone', 'birthDate', 'paymentMethod', 'installments']
        missing_fields = [key for key in campos_obrigatorios if key not in form_data or not form_data[key]]
        if missing_fields:
            logger.error(f"Campos obrigatórios ausentes: {missing_fields}")
            return JsonResponse({
                'success': False,
                'error': f'Dados incompletos. Campos obrigatórios ausentes: {", ".join(missing_fields)}'
            }, status=400)

        # Busca a atividade e departamento no banco de dados
        try:
            atividade = Atividade.objects.get(slug=form_data.get('activity'))
            departamento = Department.objects.get(slug=form_data.get('departamento').lower())
            preco_atividade = Decimal(str(atividade.preco))  # Converte para Decimal
            logger.info(f"Atividade: {atividade.nome}, Preço: {preco_atividade}")
            if preco_atividade <= 0:
                logger.error("Preço da atividade inválido")
                return JsonResponse({
                    'success': False,
                    'error': 'Preço da atividade inválido'
                }, status=400)
        except Atividade.DoesNotExist:
            logger.error(f"Atividade não encontrada: {form_data.get('activity')}")
            return JsonResponse({
                'success': False,
                'error': 'Atividade não encontrada'
            }, status=404)
        except Department.DoesNotExist:
            logger.error(f"Departamento não encontrado: {form_data.get('departamento')}")
            return JsonResponse({
                'success': False,
                'error': 'Departamento não encontrado'
            }, status=404)
        except (AttributeError, TypeError, InvalidOperation) as e:
            logger.error(f"Erro ao verificar preço da atividade: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Erro ao verificar preço da atividade'
            }, status=400)

        # Processamento do número de prestações
        try:
            numero_parcelas = int(form_data.get('installments', 1))
            logger.info(f"Número de prestações: {numero_parcelas}")
            if numero_parcelas not in [1, 2]:
                logger.error(f"Número de prestações inválido: {numero_parcelas}")
                return JsonResponse({
                    'success': False,
                    'error': 'Número de prestações inválido. Escolha 1 ou 2 prestações.'
                }, status=400)
            tipo_pagamento = 'parcelado' if numero_parcelas == 2 else 'avista'
            valor_minimo = preco_atividade if numero_parcelas == 1 else preco_atividade / 2
        except (ValueError, TypeError) as e:
            logger.error(f"Erro ao processar número de prestações: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Número de prestações inválido'
            }, status=400)

        # Processamento do pagamento
        metodo_pagamento = form_data.get('paymentMethod')
        valor_pago = None
        comprovativo = None
        TOLERANCIA = Decimal('0.1')

        if metodo_pagamento == 'mao':
            try:
                valor_entrada = form_data.get('valorEntrada', '0')
                logger.info(f"Valor entrada recebido: {valor_entrada} (tipo: {type(valor_entrada)})")
                valor_pago = Decimal(str(valor_entrada).replace(',', '.').strip())
                logger.info(f"Valor em mão convertido: {valor_pago}, Mínimo: {valor_minimo}, Total: {preco_atividade}")
                if numero_parcelas == 1 and abs(valor_pago - preco_atividade) > TOLERANCIA:
                    logger.error(f"Valor em mão inválido para 1 prestação: {valor_pago} != {preco_atividade}")
                    return JsonResponse({
                        'success': False,
                        'error': f'O valor em mão deve ser exatamente Kz {preco_atividade} para 1 prestação'
                    }, status=400)
                if numero_parcelas == 2 and (valor_pago < valor_minimo or valor_pago > preco_atividade):
                    logger.error(f"Valor em mão fora do intervalo para 2 prestações: {valor_pago}")
                    return JsonResponse({
                        'success': False,
                        'error': f'O valor em mão deve ser entre Kz {valor_minimo} e Kz {preco_atividade} para 2 prestações'
                    }, status=400)
            except (InvalidOperation, TypeError, ValueError) as e:
                logger.error(f"Erro ao processar valor_entrada: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': 'Valor em mão inválido'
                }, status=400)
                
        elif metodo_pagamento == 'transferencia':
            try:
                valor_transferencia = form_data.get('valorTransferencia', '0')
                logger.info(f"Valor transferência recebido: {valor_transferencia} (tipo: {type(valor_transferencia)})")
                valor_pago = Decimal(str(valor_transferencia).replace(',', '.').strip())
                logger.info(f"Valor transferido convertido: {valor_pago}, Mínimo: {valor_minimo}, Total: {preco_atividade}")
                if numero_parcelas == 1 and abs(valor_pago - preco_atividade) > TOLERANCIA:
                    logger.error(f"Valor transferido inválido para 1 prestação: {valor_pago} != {preco_atividade}")
                    return JsonResponse({
                        'success': False,
                        'error': f'O valor transferido deve ser exatamente Kz {preco_atividade} para 1 prestação'
                    }, status=400)
                if numero_parcelas == 2 and (valor_pago < valor_minimo or valor_pago > preco_atividade):
                    logger.error(f"Valor transferido fora do intervalo para 2 prestações: {valor_pago}")
                    return JsonResponse({
                        'success': False,
                        'error': f'O valor transferido deve ser entre Kz {valor_minimo} e Kz {preco_atividade} para 2 prestações'
                    }, status=400)
                    
                if 'comprovativo' not in request.FILES:
                    logger.error("Comprovativo de transferência ausente")
                    return JsonResponse({
                        'success': False,
                        'error': 'Comprovativo de transferência é obrigatório'
                    }, status=400)
                    
                comprovativo = request.FILES['comprovativo']
                if comprovativo.size > 2 * 1024 * 1024:  # 2MB
                    logger.error("Comprovativo excede 2MB")
                    return JsonResponse({
                        'success': False,
                        'error': 'O arquivo do comprovativo excede o limite de 2MB'
                    }, status=400)
            except (InvalidOperation, TypeError, ValueError) as e:
                logger.error(f"Erro ao processar valor_transferencia: {str(e)}")
                return JsonResponse({
                    'success': False,
                    'error': 'Valor de transferência inválido'
                }, status=400)
        else:
            logger.error(f"Método de pagamento inválido: {metodo_pagamento}")
            return JsonResponse({
                'success': False,
                'error': 'Método de pagamento inválido'
            }, status=400)

        # Gerar referência de pagamento
        referencia = f"IEL-{timezone.now().strftime('%Y%m%d')}-{Inscricao.objects.count() + 1:04d}"

        # Criação da inscrição
        inscricao = Inscricao(
            atividade=atividade,
            departamento=departamento,
            nome_completo=form_data.get('fullName'),
            email=form_data.get('email'),
            telefone=form_data.get('phone'),
            data_nascimento=form_data.get('birthDate'),
            emergencia_nome1=form_data.get('emergenciaNome1', ''),
            emergencia_telefone1=form_data.get('emergenciaTelefone1', ''),
            emergencia_nome2=form_data.get('emergenciaNome2', ''),
            emergencia_telefone2=form_data.get('emergenciaTelefone2', ''),
            observacoes=form_data.get('observations', ''),
            metodo_pagamento=metodo_pagamento,
            tipo_pagamento=tipo_pagamento,
            numero_parcelas=numero_parcelas,
            valor_entrada=valor_pago if metodo_pagamento == 'mao' and tipo_pagamento == 'avista' else None,
            valor_transferencia=valor_pago if metodo_pagamento == 'transferencia' and tipo_pagamento == 'parcelado' else None,
            total=preco_atividade,
            referencia_pagamento=referencia,
            pago=False
        )

        # Salva a inscrição para gerar o ID
        inscricao.save()

        # Salva o comprovativo se for transferência
        if metodo_pagamento == 'transferencia' and comprovativo:
            inscricao.comprovativo_transferencia.save(
                f"comprovativo_{inscricao.id}_{comprovativo.name}",
                comprovativo
            )

        # Criar prestações
        Prestacao.objects.filter(inscricao=inscricao).delete()  # Remove prestações antigas
        if numero_parcelas == 1:
            Prestacao.objects.create(
                inscricao=inscricao,
                numero=1,
                valor=preco_atividade,
                pago=True,  # Pagamento à vista (mão ou transferência) é considerado pago
                metodo_pagamento=metodo_pagamento,
                comprovativo=comprovativo if metodo_pagamento == 'transferencia' else None
            )
        else:
            Prestacao.objects.create(
                inscricao=inscricao,
                numero=1,
                valor=valor_pago,
                pago=True,  # Primeira prestação (mão ou transferência) é considerada paga
                metodo_pagamento=metodo_pagamento,
                comprovativo=comprovativo if metodo_pagamento == 'transferencia' else None
            )
            Prestacao.objects.create(
                inscricao=inscricao,
                numero=2,
                valor=preco_atividade - valor_pago,
                pago=False,
                metodo_pagamento=None  # Método da segunda prestação será definido depois
            )

        # Atualizar status pago da inscrição
        inscricao.pago = not inscricao.prestacoes.filter(pago=False).exists()
        inscricao.save()

        logger.info(f"Inscrição criada com sucesso: ID {inscricao.id}, Referência {inscricao.referencia_pagamento}")
        return JsonResponse({
            'success': True,
            'referencia': inscricao.referencia_pagamento,
            'id': inscricao.id,
            'message': f'Inscrição para {atividade.nome} confirmada!',
            'total': float(preco_atividade),
            'paid': float(inscricao.get_valor_pago()),
            'remaining': float(preco_atividade - inscricao.get_valor_pago()),
            'installments': numero_parcelas,
            'pago': inscricao.pago,
            'prestacoes': [
                {
                    'numero': p.numero,
                    'valor': float(p.valor),
                    'metodo': p.metodo_pagamento,
                    'data': p.data_criacao.strftime('%d/%m/%Y %H:%M:%S') if p.data_criacao else 'Não disponível',
                    'pago': p.pago
                } for p in inscricao.prestacoes.all()
            ]
        })

    except Exception as e:
        logger.error(f"Erro ao processar inscrição: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Ocorreu um erro ao processar sua inscrição: {str(e)}'
        }, status=500)    
# View para buscar inscrição por nome ou referência
logger = logging.getLogger(__name__)
def search_inscricao(request):
    query = request.GET.get('query', '')
    if not query:
        logger.error("Query de busca ausente")
        return JsonResponse({'success': False, 'error': 'Query de busca é obrigatória'}, status=400)

    inscricoes = Inscricao.objects.filter(
        Q(referencia_pagamento__icontains=query) | Q(nome_completo__icontains=query)
    )

    if not inscricoes.exists():
        logger.info(f"Nenhuma inscrição encontrada para query: {query}")
        return JsonResponse({'success': False, 'error': 'Inscrição não encontrada'}, status=404)

    result = []
    for i in inscricoes:
        valor_pago = i.get_valor_pago() or Decimal('0.00')
        remaining = i.total - valor_pago
        prestacao_1 = i.prestacoes.filter(numero=1).first()
        prestacao_2 = i.prestacoes.filter(numero=2).first()
        # Informações da primeira prestação
        metodo_pagamento_1 = prestacao_1.metodo_pagamento if prestacao_1 else None
        data_pagamento_1 = prestacao_1.data_criacao.strftime('%d/%m/%Y %H:%M:%S') if prestacao_1 and prestacao_1.data_criacao else 'Não disponível'
        valor_pago_1 = float(prestacao_1.valor) if prestacao_1 and prestacao_1.pago else 0.0
        # Informações da segunda prestação (se existir)
        metodo_pagamento_2 = prestacao_2.metodo_pagamento if prestacao_2 else None
        data_pagamento_2 = prestacao_2.data_criacao.strftime('%d/%m/%Y %H:%M:%S') if prestacao_2 and prestacao_2.data_criacao else 'Não disponível'
        valor_pago_2 = float(prestacao_2.valor) if prestacao_2 and prestacao_2.pago else 0.0

        prestacoes = [
            {
                'numero': 1,
                'valor': valor_pago_1,
                'metodo': metodo_pagamento_1,
                'data': data_pagamento_1,
                'pago': prestacao_1.pago if prestacao_1 else False
            }
        ]
        if i.numero_parcelas == 2:
            prestacoes.append({
                'numero': 2,
                'valor': valor_pago_2,
                'metodo': metodo_pagamento_2,
                'data': data_pagamento_2,
                'pago': prestacao_2.pago if prestacao_2 else False
            })

        result.append({
            'referencia': i.referencia_pagamento,
            'activity': i.atividade.slug,
            'fullName': i.nome_completo,
            'total': float(i.total),
            'paid': float(valor_pago),
            'remaining': float(remaining),
            'installments': i.numero_parcelas,
            'pago': i.pago,
            'prestacoes': prestacoes
        })

    logger.info(f"Inscrições encontradas: {len(result)} para query: {query}")
    return JsonResponse({'success': True, 'inscricoes': result})

@csrf_exempt
def pay_second_inscricao(request):
    if request.method == 'POST':
        reference = request.POST.get('reference')
        payment_method = request.POST.get('paymentMethod')
        amount_str = request.POST.get('amount', '0')
        try:
            amount = Decimal(amount_str.replace(',', '.'))
        except InvalidOperation:
            logger.error(f"Valor inválido para amount: {amount_str}")
            return JsonResponse({'success': False, 'error': 'Valor inválido'}, status=400)

        try:
            inscricao = Inscricao.objects.get(referencia_pagamento=reference)
            valor_pago_atual = inscricao.get_valor_pago() or Decimal('0.00')
            remaining = inscricao.total - valor_pago_atual
            if remaining <= 0 or inscricao.pago:
                logger.warning(f"Inscrição já paga: {reference}")
                return JsonResponse({'success': False, 'error': 'Inscrição já está totalmente paga'}, status=400)

            if abs(amount - remaining) > Decimal('0.1'):
                logger.error(f"Valor incorreto para segunda prestação: {amount} != {remaining}")
                return JsonResponse({'success': False, 'error': f'O valor deve ser exatamente Kz {remaining}'}, status=400)

            comprovativo = None
            if payment_method == 'transferencia':
                if 'comprovativo' not in request.FILES:
                    logger.error("Comprovativo ausente para transferência")
                    return JsonResponse({'success': False, 'error': 'Comprovativo é obrigatório para transferência'}, status=400)
                comprovativo = request.FILES['comprovativo']
                if comprovativo.size > 2 * 1024 * 1024:
                    logger.error("Comprovativo excede 2MB")
                    return JsonResponse({'success': False, 'error': 'O arquivo do comprovativo excede o limite de 2MB'}, status=400)

            # Atualizar a segunda prestação
            prestacao = inscricao.prestacoes.filter(numero=2).first()
            if not prestacao:
                logger.error("Segunda prestação não encontrada")
                return JsonResponse({'success': False, 'error': 'Segunda prestação não encontrada'}, status=400)

            prestacao.valor = amount
            prestacao.pago = True
            prestacao.metodo_pagamento = payment_method
            if comprovativo:
                prestacao.comprovativo.save(f"comprovativo_segunda_{inscricao.id}_{comprovativo.name}", comprovativo)
            prestacao.save()

            # Atualizar status da inscrição
            inscricao.pago = not inscricao.prestacoes.filter(pago=False).exists()
            inscricao.save()

            logger.info(f"Segunda prestação paga com sucesso para inscrição {reference}")
            prestacao_1 = inscricao.prestacoes.filter(numero=1).first()
            prestacao_2 = inscricao.prestacoes.filter(numero=2).first()
            return JsonResponse({
                'success': True,
                'message': 'Segunda prestação paga com sucesso',
                'referencia': inscricao.referencia_pagamento,
                'id': inscricao.id,
                'activity': inscricao.atividade.nome,
                'fullName': inscricao.nome_completo,
                'total': float(inscricao.total),
                'paid': float(inscricao.get_valor_pago()),
                'remaining': float(inscricao.total - inscricao.get_valor_pago()),
                'pago': inscricao.pago,
                'installments': inscricao.numero_parcelas,
                'prestacoes': [
                    {
                        'numero': 1,
                        'valor': float(prestacao_1.valor) if prestacao_1 else 0.0,
                        'metodo': prestacao_1.metodo_pagamento if prestacao_1 else None,
                        'data': prestacao_1.data_criacao.strftime('%d/%m/%Y %H:%M:%S') if prestacao_1 and prestacao_1.data_criacao else 'Não disponível',
                        'pago': prestacao_1.pago if prestacao_1 else False
                    },
                    {
                        'numero': 2,
                        'valor': float(prestacao_2.valor) if prestacao_2 else 0.0,
                        'metodo': prestacao_2.metodo_pagamento if prestacao_2 else None,
                        'data': prestacao_2.data_criacao.strftime('%d/%m/%Y %H:%M:%S') if prestacao_2 and prestacao_2.data_criacao else 'Não disponível',
                        'pago': prestacao_2.pago if prestacao_2 else False
                    } if inscricao.numero_parcelas == 2 else None
                ]
            })

        except Inscricao.DoesNotExist:
            logger.error(f"Inscrição não encontrada: {reference}")
            return JsonResponse({'success': False, 'error': 'Inscrição não encontrada'}, status=404)
        except Exception as e:
            logger.error(f"Erro ao processar segunda prestação: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    logger.error("Método inválido para pay_second_inscricao")
    return JsonResponse({'success': False, 'error': 'Método inválido'}, status=400)

@require_POST
def pagar_prestacao(request, referencia):
    try:
        inscricao = Inscricao.objects.get(referencia_pagamento=referencia)
        data = json.loads(request.POST.get('formData'))
        
        prestacao = inscricao.prestacoes.filter(numero=data['numero_prestacao'], pago=False).first()
        if not prestacao:
            return JsonResponse({'success': False, 'error': 'Prestação já paga ou não encontrada'})

        prestacao.valor = float(data['valor'])
        prestacao.data_pagamento = timezone.now()
        prestacao.pago = True
        
        if 'comprovativo' in request.FILES:
            comprovativo = request.FILES['comprovativo']
            prestacao.comprovativo.save(comprovativo.name, comprovativo)
        
        prestacao.save()

        # Atualizar inscricao.total com base em todas as prestações pagas
        total_prestacoes = sum(p.valor for p in inscricao.prestacoes.filter(pago=True))
        inscricao.total = (inscricao.valor_entrada or 0) + (inscricao.valor_transferencia or 0) + total_prestacoes
        inscricao.pago = not inscricao.prestacoes.filter(pago=False).exists()
        inscricao.save()
        
        return JsonResponse({'success': True, 'pago_completo': inscricao.pago, 'total': str(inscricao.total)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_GET
def consultar_inscricao(request, referencia):
    try:
        inscricao = Inscricao.objects.get(referencia_pagamento=referencia)
        prestacoes = inscricao.prestacoes.all().values('numero', 'valor', 'data_esperada', 'data_pagamento', 'pago')
        return JsonResponse({'success': True, 'prestacoes': list(prestacoes), 'pago': inscricao.pago})
    except Inscricao.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Inscrição não encontrada'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
def get_precos_atividades(request):
    atividades = Atividade.objects.all().values('slug', 'preco')
    return JsonResponse(list(atividades), safe=False)

def lista_atividades(request):
    atividades = Atividade.objects.all().values()
    return JsonResponse(list(atividades), safe=False)

    
############################ADMINISTRATIVO VIEWS#####################################

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def marcar_feita(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        carta_id = data.get('id')
        try:
            carta = Carta.objects.get(id=carta_id)
            carta.foi_feita = True
            carta.data_conclusao = timezone.now()
            carta.save()
            logger.info(f"Carta {carta_id} marcada como concluída")
            return JsonResponse({'status': 'success'})
        except Carta.DoesNotExist:
            logger.error(f"Carta {carta_id} não encontrada")
            return JsonResponse({'status': 'error', 'message': 'Carta não encontrada'}, status=404)
    logger.warning(f"Método inválido para marcar_feita: {request.method}")
    return JsonResponse({'status': 'error', 'message': 'Método inválido'}, status=400)

@csrf_exempt
@login_required
def visualizar_carta(request, carta_id):
    try:
        carta = Carta.objects.get(id=carta_id)
        data = {
            'status': 'success',
            'carta': {
                'referencia': carta.referencia,
                'nome': carta.nome,
                'email': carta.email,
                'destino': carta.destino,
                'objectivo': carta.objectivo,
                'tipo_carta': carta.tipo_carta,
                'telefone': carta.telefone,
                'data_solicitacao': carta.data_solicitacao.strftime('%d/%m/%Y %H:%M'),
                'foi_feita': carta.foi_feita,
                'outras_inf': carta.outras_inf
            }
        }
        logger.info(f"Visualização da carta {carta_id} bem-sucedida")
        return JsonResponse(data)
    except Carta.DoesNotExist:
        logger.error(f"Carta {carta_id} não encontrada para visualização")
        return JsonResponse({'status': 'error', 'message': 'Carta não encontrada'}, status=404)

@csrf_exempt
@login_required
def editar_carta(request, carta_id):
    if request.method == 'POST':
        try:
            carta = Carta.objects.get(id=carta_id)
            data = json.loads(request.body)
            carta.nome = data.get('nome', carta.nome)
            carta.email = data.get('email', carta.email)
            carta.destino = data.get('destino', carta.destino)
            carta.objectivo = data.get('objectivo', carta.objectivo)
            carta.tipo_carta = data.get('tipo_carta', carta.tipo_carta)
            carta.telefone = data.get('telefone', carta.telefone)
            carta.outras_inf = data.get('outras_inf', carta.outras_inf)
            # Se tipo_carta mudou, regenerar referência
            if data.get('tipo_carta') and data['tipo_carta'] != carta.tipo_carta:
                carta.referencia = None  # Forçar nova geração de referência
            carta.save()
            logger.info(f"Carta {carta_id} editada com sucesso")
            return JsonResponse({'status': 'success'})
        except Carta.DoesNotExist:
            logger.error(f"Carta {carta_id} não encontrada para edição")
            return JsonResponse({'status': 'error', 'message': 'Carta não encontrada'}, status=404)
        except Exception as e:
            logger.error(f"Erro ao editar carta {carta_id}: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Erro ao editar a carta'}, status=400)
    logger.warning(f"Método inválido para editar_carta: {request.method}")
    return JsonResponse({'status': 'error', 'message': 'Método inválido'}, status=400)

@csrf_exempt
@login_required
def deletar_carta(request, carta_id):
    if request.method == 'POST':
        try:
            carta = Carta.objects.get(id=carta_id)
            carta.delete()
            logger.info(f"Carta {carta_id} deletada com sucesso")
            return JsonResponse({'status': 'success'})
        except Carta.DoesNotExist:
            logger.error(f"Carta {carta_id} não encontrada para deleção")
            return JsonResponse({'status': 'error', 'message': 'Carta não encontrada'}, status=404)
    logger.warning(f"Método inválido para deletar_carta: {request.method}")
    return JsonResponse({'status': 'error', 'message': 'Método inválido'}, status=400)

logger = logging.getLogger(__name__)
class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'webiel/pages/dashboard.html'
    model = Carta
    context_object_name = 'cartas'
    paginate_by = 10

    def get_queryset(self):
        # Filtra apenas cartas pendentes (foi_feita=False) por padrão
        queryset = Carta.objects.filter(foi_feita=False).order_by('-data_solicitacao')
        search = self.request.GET.get('search', '')
        tipo = self.request.GET.get('tipo', '')
        referencia = self.request.GET.get('referencia', '')
        data_filtro = self.request.GET.get('data', '')

        if search:
            queryset = queryset.filter(
                models.Q(nome__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(referencia__icontains=search)
            )
        if tipo:
            queryset = queryset.filter(tipo_carta__iexact=tipo)
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)
        if data_filtro:
            try:
                data = datetime.strptime(data_filtro, '%Y-%m-%d').date()
                queryset = queryset.filter(data_solicitacao__date=data)
            except ValueError:
                logger.warning(f"Formato de data inválido: {data_filtro}")

        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pendentes'] = Carta.objects.filter(foi_feita=False).count()
        context['total_feitas'] = Carta.objects.filter(foi_feita=True).count()
        context['total_geral'] = Carta.objects.all().count()
        context['tipos_carta'] = Carta.objects.values_list('tipo_carta', flat=True).distinct()
        context['search'] = self.request.GET.get('search', '')
        context['tipo'] = self.request.GET.get('tipo', '')
        context['referencia'] = self.request.GET.get('referencia', '')
        context['data'] = self.request.GET.get('data', '')
        return context

    def get(self, request, *args, **kwargs):
        logger.debug(f"Requisição recebida: AJAX={request.headers.get('X-Requested-With')}, GET params={request.GET}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                queryset = self.get_queryset()
                cartas = [{
                    'id': carta.id,
                    'referencia': carta.referencia or '-',
                    'nome': carta.nome or '-',
                    'email': carta.email or '-',
                    'destino': carta.destino or '-',
                    'objectivo': carta.objectivo or '-',
                    'tipo_carta': carta.tipo_carta or '-',
                    'telefone': carta.telefone or '-',
                    'data_solicitacao': carta.data_solicitacao.strftime('%d/%m/%Y %H:%M') if carta.data_solicitacao else '-',
                    'outras_inf': carta.outras_inf or '-'
                } for carta in queryset]
                
                response_data = {
                    'success': True,
                    'cartas': cartas,
                    'total_pendentes': Carta.objects.filter(foi_feita=False).count(),
                    'total_feitas': Carta.objects.filter(foi_feita=True).count(),
                    'total_geral': Carta.objects.all().count()
                }
                logger.debug(f"Resposta JSON: {response_data}")
                return JsonResponse(response_data, status=200)
            except Exception as e:
                logger.error(f"Erro ao processar requisição AJAX: {str(e)}")
                return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
        return super().get(request, *args, **kwargs)

logger = logging.getLogger(__name__)
class CartasFeitasView(LoginRequiredMixin, ListView):
    template_name = 'webiel/pages/cartas_feitas.html'
    model = Carta
    context_object_name = 'cartas'
    paginate_by = 10

    def get_queryset(self):
        queryset = Carta.objects.filter(foi_feita=True).order_by('-data_solicitacao')
        # Suporte a filtros dinâmicos
        search = self.request.GET.get('search', '')
        tipo = self.request.GET.get('tipo', '')

        if search:
            queryset = queryset.filter(nome__icontains=search) | queryset.filter(email__icontains=search)
        if tipo:
            queryset = queryset.filter(tipo_carta__iexact=tipo)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pendentes'] = Carta.objects.filter(foi_feita=False).count()
        context['total_feitas'] = Carta.objects.filter(foi_feita=True).count()
        context['total_geral'] = Carta.objects.all().count()
        context['tipos_carta'] = Carta.objects.values_list('tipo_carta', flat=True).distinct()
        return context

        if search:
            queryset = queryset.filter(
                models.Q(nome__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(referencia__icontains=search)
            )
        if tipo:
            queryset = queryset.filter(tipo_carta__iexact=tipo)
        if referencia:
            queryset = queryset.filter(referencia__icontains=referencia)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pendentes'] = Carta.objects.filter(foi_feita=False).count()
        context['total_feitas'] = Carta.objects.filter(foi_feita=True).count()
        context['total_geral'] = Carta.objects.all().count()
        context['tipos_carta'] = Carta.objects.values_list('tipo_carta', flat=True).distinct()
        context['search'] = self.request.GET.get('search', '')
        context['tipo'] = self.request.GET.get('tipo', '')
        context['referencia'] = self.request.GET.get('referencia', '')
        return context

def custom_logout(request):
    logout(request)
    messages.success(request, 'Você saiu com Sucesso!')
    return redirect('webiel:login')

logger = logging.getLogger(__name__)
class CriarPublicacaoView(LoginRequiredMixin, CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'webiel/pages/publicacao.html'
    success_url = reverse_lazy('webiel:publicacoes')

    def form_valid(self, form):
        try:
            logger.debug('Formulário válido, processando...')
            # Define o autor
            form.instance.author = self.request.user
            # Gera um slug único
            base_slug = slugify(form.instance.title)
            slug = base_slug
            counter = 1
            while Noticia.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            form.instance.slug = slug

            # Salva a instância
            form.instance.save()
            logger.info(f"Publicação criada: {form.instance.id}, slug: {slug}")

            # Verifica se é uma requisição AJAX
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Publicação criada com sucesso!'
                }, json_dumps_params={'ensure_ascii': False})
            else:
                messages.success(self.request, 'Publicação criada com sucesso!')
                return super().form_valid(form)
        except Exception as e:
            logger.error(f"Erro ao criar publicação: {str(e)}")
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': f'Erro interno: {str(e)}'
                }, status=500, json_dumps_params={'ensure_ascii': False})
            else:
                messages.error(self.request, f'Erro interno: {str(e)}')
                return self.form_invalid(form)

    def form_invalid(self, form):
        logger.error(f"Erros no formulário: {form.errors.as_json()}")
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Erro ao criar a publicação. Verifique os campos e tente novamente.',
                'errors': json.loads(form.errors.as_json())
            }, status=400, json_dumps_params={'ensure_ascii': False})
        else:
            messages.error(self.request, 'Erro ao criar a publicação. Verifique os campos e tente novamente.')
            return super().form_invalid(form)

    def form_invalid(self, form):
        logger.error(f"Erros no formulário: {form.errors.as_json()}")
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'Erro ao criar a publicação. Verifique os campos e tente novamente.',
                'errors': json.loads(form.errors.as_json())
            }, status=400)
        else:
            messages.error(self.request, 'Erro ao criar a publicação. Verifique os campos e tente novamente.')
            return super().form_invalid(form)

logger = logging.getLogger(__name__)
class PublicacoesListView(LoginRequiredMixin, ListView):
    model = Noticia
    template_name = 'webiel/pages/publicacoes.html'
    context_object_name = 'publicacoes'
    ordering = ['-created_at']  # Corrigido o erro de digitação 'creted_at'
    paginate_by = 10  # 10 publicações por página

    def get_queryset(self):
        queryset = Noticia.objects.all().select_related('category', 'author')
        # Obter parâmetros de filtro da URL
        search = self.request.GET.get('search', '').strip()
        status = self.request.GET.get('status', '')
        categoria = self.request.GET.get('categoria', '')

        logger.debug(f"Parâmetros de filtro recebidos: search={search}, status={status}, categoria={categoria}")

        # Aplicar filtro de busca
        if search:
            queryset = queryset.filter(Q(title__icontains=search))
            logger.debug(f"Filtro de busca aplicado: {search}")

        # Aplicar filtro de status
        if status in ('published', 'hidden'):
            is_published = status == 'published'
            queryset = queryset.filter(is_published=is_published)
            logger.debug(f"Filtro de status aplicado: is_published={is_published}")

        # Aplicar filtro de categoria
        if categoria:
            try:
                queryset = queryset.filter(category_id=categoria)
                logger.debug(f"Filtro de categoria aplicado: categoria_id={categoria}")
            except ValueError:
                logger.warning(f"ID de categoria inválido: {categoria}")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar categorias ao contexto para o filtro
        context['categorias'] = Category.objects.all()
        logger.debug(f"Contexto enviado: {len(context['categorias'])} categorias carregadas")
        return context

logger = logging.getLogger(__name__)
class EditarPublicacaoView(LoginRequiredMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'webiel/pages/editar_publicacao.html'
    success_url = reverse_lazy('webiel:publicacoes')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Temporariamente removida a restrição de autor para testes
        queryset = Noticia.objects.all()
        logger.debug(f"Usuário: {self.request.user}, Queryset: {queryset.count()} publicações")
        return queryset

    def form_valid(self, form):
        form.instance.author = self.request.user
        base_slug = slugify(form.instance.title)
        slug = base_slug
        counter = 1
        while Noticia.objects.filter(slug=slug).exclude(slug=self.object.slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        form.instance.slug = slug
        logger.debug(f"Salvando publicação com slug: {slug}")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj:
            logger.error(f"Publicação não encontrada para slug: {self.kwargs.get('slug')}")
            raise Noticia.DoesNotExist("Publicação não encontrada.")
        logger.debug(f"Objeto encontrado: {obj.title}, slug: {obj.slug}")
        return obj

class DeletarPublicacaoView(LoginRequiredMixin, DeleteView):
    model = Noticia
    success_url = reverse_lazy('webiel:publicacoes')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Temporariamente removida a restrição de autor para testes
        queryset = Noticia.objects.all()
        logger.debug(f"Usuário: {self.request.user}, Queryset para exclusão: {queryset.count()} publicações")
        return queryset
    def post(self, request, *args, **kwargs):
     
     return self.delete(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            logger.debug(f"Excluindo publicação: {self.object.title}, slug: {self.object.slug}")
            self.object.delete()
            return JsonResponse({
                'success': True,
                'message': 'Publicação excluída com sucesso!',
                'redirect_url': success_url
            })
        except Noticia.DoesNotExist:
            logger.error(f"Publicação não encontrada para slug: {self.kwargs.get('slug')}")
            return JsonResponse({
                'success': False,
                'message': 'Publicação não encontrada.'
            }, status=404)
        except Exception as e:
            logger.error(f"Erro ao excluir publicação: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Erro ao excluir: {str(e)}'
            }, status=500)

logger = logging.getLogger(__name__)        
class CriarFotoView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'webiel/pages/criar_foto.html'
    success_url = reverse_lazy('webiel:criar_foto')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        else:
            form.instance.author = None  # Fallback, though LoginRequiredMixin should prevent this
        response = super().form_valid(form)
        messages.success(self.request, 'Foto enviada com sucesso!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao enviar a foto. Verifique os campos e tente novamente.')
        return super().form_invalid(form)

@require_POST
@csrf_exempt
def toggle_publicacao(request):
    try:
        print(f"Requisição recebida para /publicacoes/toggle/")  # Log para depuração
        data = json.loads(request.body)
        publicacao_id = data.get('publicacao_id')
        print(f"Recebido publicacao_id: {publicacao_id}")  # Log para depuração
        if not publicacao_id:
            return JsonResponse({'success': False, 'message': 'ID da publicação não fornecido.'}, status=400)
        
        try:
            publicacao = Noticia.objects.get(id=publicacao_id)
            print(f"Publicação encontrada: {publicacao.title} (ID: {publicacao.id})")  # Log para depuração
        except Noticia.DoesNotExist:
            print(f"Publicação com ID {publicacao_id} não encontrada")  # Log para depuração
            return JsonResponse({'success': False, 'message': 'Publicação não encontrada.'}, status=404)
        
        publicacao.is_published = not publicacao.is_published
        publicacao.save()
        print(f"Status atualizado para is_published: {publicacao.is_published}")  # Log para depuração
        
        return JsonResponse({
            'success': True,
            'is_published': publicacao.is_published,
            'message': f'Publicação {"publicada" if publicacao.is_published else "oculta"} com sucesso!'
        })
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON")  # Log para depuração
        return JsonResponse({'success': False, 'message': 'Erro ao processar os dados da requisição.'}, status=400)
    except Exception as e:
        print(f"Erro interno: {str(e)}")  # Log para depuração
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
    
class NubentesListView(LoginRequiredMixin, ListView):
    model = Casamento
    template_name = 'webiel/pages/nubentes.html'
    context_object_name = 'nubentes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        ano = self.request.GET.get('ano')
        nome = self.request.GET.get('nome')
        if ano:
            queryset = queryset.filter(data_casam__year=ano)
        if nome:
            queryset = queryset.filter(
                models.Q(nome_noivo__icontains=nome) | 
                models.Q(nome_noiva__icontains=nome)
            )
        return queryset.order_by('data_casam')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ano'] = self.request.GET.get('ano', '')
        context['nome'] = self.request.GET.get('nome', '')
        three_months_from_now = timezone.now().date() + timedelta(days=90)
        upcoming_weddings = Casamento.objects.filter(
            data_casam__lte=three_months_from_now,
            data_casam__gte=timezone.now().date()
        )
        context['upcoming_weddings_count'] = upcoming_weddings.count()
        context['upcoming_wedding_ids'] = list(upcoming_weddings.values_list('id', flat=True))
        return context

@require_GET
def nubente_detalhes(request):
    try:
        print(f"Requisição recebida para /nubentes/detalhes/")  # Log para depuração
        nubente_id = request.GET.get('id')
        print(f"Recebido nubente_id: {nubente_id}")  # Log para depuração
        if not nubente_id:
            return JsonResponse({'success': False, 'message': 'ID do nubente não fornecido.'}, status=400)
        
        try:
            nubente = Casamento.objects.get(id=nubente_id)
            print(f"Nubente encontrado: {nubente}")  # Log para depuração
            return JsonResponse({
                'success': True,
                'nubente': {
                    'nome_noivo': nubente.nome_noivo,
                    'nome_noiva': nubente.nome_noiva,
                    'telefone': nubente.telefone,
                    'data_casam': nubente.data_casam.strftime('%Y-%m-%d')
                }
            })
        except Casamento.DoesNotExist:
            print(f"Nubente com ID {nubente_id} não encontrado")  # Log para depuração
            return JsonResponse({'success': False, 'message': 'Nubente não encontrado.'}, status=404)
    except Exception as e:
        print(f"Erro interno: {str(e)}")  # Log para depuração
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

@require_POST
@csrf_exempt
def nubente_editar(request):
    try:
        print(f"[{timezone.now()}] Requisição recebida para /nubentes/editar/")  # Log com timestamp
        data = json.loads(request.body)
        print(f"[{timezone.now()}] Dados recebidos: {data}")  # Log dos dados brutos
        
        nubente_id = data.get('nubente_id')
        nome_noivo = data.get('nome_noivo')
        nome_noiva = data.get('nome_noiva')
        telefone = data.get('telefone')
        data_casam = data.get('data_casam')

        # Validação de campos obrigatórios
        if not all([nubente_id, nome_noivo, nome_noiva, telefone, data_casam]):
            print(f"[{timezone.now()}] Erro: Campos obrigatórios faltando")  # Log
            return JsonResponse({
                'success': False,
                'message': 'Todos os campos (ID, nome do noivo, nome da noiva, telefone, data do casamento) são obrigatórios.'
            }, status=400)

        # Validação do formato da data
        try:
            data_casam = datetime.strptime(data_casam, '%Y-%m-%d').date()
            print(f"[{timezone.now()}] Data validada: {data_casam}")  # Log
        except ValueError as e:
            print(f"[{timezone.now()}] Erro de formato de data: {str(e)}")  # Log
            return JsonResponse({
                'success': False,
                'message': f'Formato de data inválido. Use YYYY-MM-DD (ex.: 2025-07-01).'
            }, status=400)

        # Buscar e atualizar o nubente
        try:
            nubente = Casamento.objects.get(id=nubente_id)
            print(f"[{timezone.now()}] Nubente encontrado: {nubente}")  # Log
            nubente.nome_noivo = nome_noivo.strip()
            nubente.nome_noiva = nome_noiva.strip()
            nubente.telefone = telefone.strip()
            nubente.data_casam = data_casam
            nubente.save()
            print(f"[{timezone.now()}] Nubente atualizado: {nubente}")  # Log
            return JsonResponse({
                'success': True,
                'message': 'Nubente actualizado com sucesso!',
                'nubente': {
                    'nome_noivo': nubente.nome_noivo,
                    'nome_noiva': nubente.nome_noiva,
                    'telefone': nubente.telefone,
                    'data_casam': nubente.data_casam.strftime('%d/%m/%Y')
                }
            })
        except Casamento.DoesNotExist:
            print(f"[{timezone.now()}] Nubente com ID {nubente_id} não encontrado")  # Log
            return JsonResponse({
                'success': False,
                'message': f'Nubente com ID {nubente_id} não encontrado.'
            }, status=404)
        except IntegrityError as e:
            print(f"[{timezone.now()}] Erro de integridade: {str(e)}")  # Log
            return JsonResponse({
                'success': False,
                'message': f'Erro: Dados fornecidos violam restrições do banco (ex.: telefone já em uso).'
            }, status=400)
    except json.JSONDecodeError as e:
        print(f"[{timezone.now()}] Erro ao decodificar JSON: {str(e)}")  # Log
        return JsonResponse({
            'success': False,
            'message': 'Erro ao processar os dados da requisição. Verifique o formato JSON.'
        }, status=400)
    except Exception as e:
        print(f"[{timezone.now()}] Erro interno: {str(e)}")  # Log
        return JsonResponse({
            'success': False,
            'message': f'Erro interno no servidor: {str(e)}'
        }, status=500)

@require_POST
@csrf_exempt
def nubente_deletar(request):
    try:
        print(f"Requisição recebida para /nubentes/deletar/")  # Log para depuração
        data = json.loads(request.body)
        nubente_id = data.get('nubente_id')
        print(f"Recebido nubente_id: {nubente_id}")  # Log para depuração
        
        if not nubente_id:
            return JsonResponse({'success': False, 'message': 'ID do nubente não fornecido.'}, status=400)
        
        try:
            nubente = Casamento.objects.get(id=nubente_id)
            print(f"Nubente encontrado para exclusão: {nubente}")  # Log para depuração
            nubente.delete()
            print(f"Nubente ID {nubente_id} excluído com sucesso")  # Log para depuração
            return JsonResponse({'success': True, 'message': 'Nubente excluído com sucesso!'})
        except Casamento.DoesNotExist:
            print(f"Nubente com ID {nubente_id} não encontrado")  # Log para depuração
            return JsonResponse({'success': False, 'message': 'Nubente não encontrado.'}, status=404)
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON")  # Log para depuração
        return JsonResponse({'success': False, 'message': 'Erro ao processar os dados da requisição.'}, status=400)
    except Exception as e:
        print(f"Erro interno: {str(e)}")  # Log para depuração
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

logger = logging.getLogger(__name__)    
class DownloadNubentesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ano = request.GET.get('ano')
        queryset = Casamento.objects.all().order_by('-data_casam')
        
        if ano:
            try:
                ano = int(ano)
                queryset = queryset.filter(data_casam__year=ano)
                filename = f"nubentes_{ano}.pdf"
                logger.debug(f"Download PDF para ano: {ano}, resultados: {queryset.count()}")
            except ValueError:
                filename = f"nubentes_{datetime.now().year}.pdf"
                logger.warning(f"Valor de ano inválido para download: {ano}")
        else:
            filename = f"nubentes_{datetime.now().year}.pdf"

        # Criar resposta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Configurar PDF com reportlab
        doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm, topMargin=20*mm, bottomMargin=20*mm)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='Title',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            alignment=1,  # Centralizado
            spaceAfter=12,
            textColor=colors.HexColor('#007bff')
        )
        header_style = ParagraphStyle(
            name='Header',
            fontName='Helvetica-Bold',
            fontSize=10,
            textColor=colors.white
        )
        cell_style = ParagraphStyle(
            name='Cell',
            fontName='Helvetica',
            fontSize=9,
            leading=12
        )

        # Título
        title_text = f"Lista de Nubentes{' - ' + str(ano) if ano else ''}"
        elements.append(Paragraph(title_text, title_style))

        # Dados da tabela
        data = [['Noivo', 'Noiva', 'Telefone', 'Data do Casamento']]
        for nubente in queryset:
            data.append([
                Paragraph(nubente.nome_noivo, cell_style),
                Paragraph(nubente.nome_noiva, cell_style),
                Paragraph(nubente.telefone, cell_style),
                Paragraph(nubente.data_casam.strftime('%d/%m/%Y'), cell_style)
            ])

        # Criar tabela
        table = Table(data, colWidths=[60*mm, 60*mm, 40*mm, 30*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),  # Cabeçalho azul
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texto branco no cabeçalho
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alinhamento à esquerda
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte negrito no cabeçalho
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),  # Fundo claro
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Bordas cinza
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinhamento vertical central
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f1f1')]),  # Linhas alternadas
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)

        # Gerar PDF
        doc.build(elements)
        return response

logger = logging.getLogger(__name__)
class BancoDeAlimentacaoListView(LoginRequiredMixin, ListView):
    model = BancoDeAlimentacao
    template_name = 'webiel/pages/banco_de_alimentacao.html'
    context_object_name = 'doadores'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = BancoDeAlimentacao.objects.all()
        nome = self.request.GET.get('nome')
        bairro = self.request.GET.get('bairro')

        if nome:
            queryset = queryset.filter(nome__icontains=nome)
            logger.debug(f"Filtro por nome: {nome}, resultados: {queryset.count()}")

        if bairro:
            queryset = queryset.filter(bairro__icontains=bairro)
            logger.debug(f"Filtro por bairro: {bairro}, resultados: {queryset.count()}")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome'] = self.request.GET.get('nome', '')
        context['bairro'] = self.request.GET.get('bairro', '')
        # Calcular doações recentes (15 dias)
        today = datetime.now()
        fifteen_days_ago = today - timedelta(days=15)
        recent_donations = BancoDeAlimentacao.objects.filter(
            created_at__gte=fifteen_days_ago
        )
        context['recent_donations_count'] = recent_donations.count()
        context['recent_ids'] = list(recent_donations.values_list('id', flat=True))
        logger.debug(f"Doações recentes (15 dias): {context['recent_donations_count']}")
        context['today'] = today.date()
        return context
logger = logging.getLogger(__name__)
class DownloadBancoDeAlimentacaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        nome = request.GET.get('nome')
        bairro = request.GET.get('bairro')
        queryset = BancoDeAlimentacao.objects.all().order_by('-created_at')
        
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        if bairro:
            queryset = queryset.filter(bairro__icontains=bairro)
            
        filename = f"doadores_{datetime.now().year}.pdf"
        logger.debug(f"Download PDF para doadores, resultados: {queryset.count()}")

        # Criar resposta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Configurar PDF com reportlab
        doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=15*mm, leftMargin=15*mm, topMargin=20*mm, bottomMargin=20*mm)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='Title',
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            alignment=1,  # Centralizado
            textColor=colors.HexColor('#007bff'),
            space_after=12
        )
        cell_style = ParagraphStyle(
            name='Cell',
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            wordWrap='CJK'
        )

        # Título
        title_text = "Lista do Banco de Alimentação"
        elements.append(Paragraph(title_text, title_style))

        # Dados da tabela
        data = [['Nome', 'Email', 'Telefone', 'Bairro', 'Donativo']]
        for doador in queryset:
            data.append([
                Paragraph(doador.nome, cell_style),
                Paragraph(doador.email, cell_style),
                Paragraph(doador.telefone, cell_style),
                Paragraph(doador.bairro, cell_style),
                Paragraph(doador.donativo[:100], cell_style)  # Limitar para evitar overflow
            ])

        table = Table(data, colWidths=[40*mm, 40*mm, 30*mm, 30*mm, 50*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f1f1')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(table)

        # Gerar PDF
        doc.build(elements)
        return response

logger = logging.getLogger(__name__)
class MensagensNewsletterView(LoginRequiredMixin, View):
    template_name = 'webiel/pages/mensagens_newsletter.html'
    paginate_by = 10  # 10 itens por página

    def get(self, request, *args, **kwargs):
        # Lógica de notificações
        last_visit = self.request.session.get('mensagens_newsletter_last_visit')
        current_time = timezone.now()
        self.request.session['mensagens_newsletter_last_visit'] = current_time.isoformat()

        # Obter parâmetros de pesquisa
        mensagem_nome = self.request.GET.get('mensagem_nome', '').strip()
        mensagem_email = self.request.GET.get('mensagem_email', '').strip()
        newsletter_email = self.request.GET.get('newsletter_email', '').strip()

        # Querysets com filtros
        mensagens = Mensagem.objects.all().order_by('-created_at')
        if mensagem_nome:
            mensagens = mensagens.filter(nome__icontains=mensagem_nome)
        if mensagem_email:
            mensagens = mensagens.filter(email__icontains=mensagem_email)

        newsletters = Newsletter.objects.all().order_by('-created_at')
        if newsletter_email:
            newsletters = newsletters.filter(email__icontains=newsletter_email)

        # Contagem de novos registros (baseado no queryset sem filtros para notificações)
        new_mensagens = Mensagem.objects.filter(created_at__gt=last_visit).count() if last_visit else 0
        new_newsletters = Newsletter.objects.filter(created_at__gt=last_visit).count() if last_visit else 0
        notification_message = None
        if new_mensagens > 0 or new_newsletters > 0:
            parts = []
            if new_mensagens > 0:
                parts.append(f"{new_mensagens} nova(s) mensagem(ns)")
            if new_newsletters > 0:
                parts.append(f"{new_newsletters} novo(s) e-mail(s) na newsletter")
            notification_message = "Você tem " + " e ".join(parts) + "!"

        # Paginação para Mensagens
        mensagem_paginator = Paginator(mensagens, self.paginate_by)
        mensagem_page_number = self.request.GET.get('mensagem_page', 1)
        mensagem_page_obj = mensagem_paginator.get_page(mensagem_page_number)

        # Paginação para Newsletter
        newsletter_paginator = Paginator(newsletters, self.paginate_by)
        newsletter_page_number = self.request.GET.get('newsletter_page', 1)
        newsletter_page_obj = newsletter_paginator.get_page(newsletter_page_number)

        # Contexto
        context = {
            'data': {
                'mensagens': mensagem_page_obj,
                'newsletters': newsletter_page_obj,
                'notification_message': notification_message,
            },
            'mensagem_paginator': mensagem_page_obj,
            'newsletter_paginator': newsletter_page_obj,
            'mensagem_nome': mensagem_nome,
            'mensagem_email': mensagem_email,
            'newsletter_email': newsletter_email,
            'user': self.request.user
        }
        return render(self.request, self.template_name, context)
    template_name = 'webiel/pages/mensagens_newsletter.html'
    paginate_by = 10  # 10 itens por página

    def get(self, request, *args, **kwargs):
        # Lógica de notificações
        last_visit = self.request.session.get('mensagens_newsletter_last_visit')
        current_time = timezone.now()
        self.request.session['mensagens_newsletter_last_visit'] = current_time.isoformat()

        # Querysets
        mensagens = Mensagem.objects.all().order_by('-created_at')
        newsletters = Newsletter.objects.all().order_by('-created_at')

        # Contagem de novos registros
        new_mensagens = Mensagem.objects.filter(created_at__gt=last_visit).count() if last_visit else 0
        new_newsletters = Newsletter.objects.filter(created_at__gt=last_visit).count() if last_visit else 0
        notification_message = None
        if new_mensagens > 0 or new_newsletters > 0:
            parts = []
            if new_mensagens > 0:
                parts.append(f"{new_mensagens} nova(s) mensagem(ns)")
            if new_newsletters > 0:
                parts.append(f"{new_newsletters} novo(s) e-mail(s) na newsletter")
            notification_message = "Você tem " + " e ".join(parts) + "!"

        # Paginação para Mensagens
        mensagem_paginator = Paginator(mensagens, self.paginate_by)
        mensagem_page_number = self.request.GET.get('mensagem_page', 1)
        mensagem_page_obj = mensagem_paginator.get_page(mensagem_page_number)

        # Paginação para Newsletter
        newsletter_paginator = Paginator(newsletters, self.paginate_by)
        newsletter_page_number = self.request.GET.get('newsletter_page', 1)
        newsletter_page_obj = newsletter_paginator.get_page(newsletter_page_number)

        # Contexto
        context = {
            'data': {
                'mensagens': mensagem_page_obj,
                'newsletters': newsletter_page_obj,
                'notification_message': notification_message,
            },
            'mensagem_paginator': mensagem_page_obj,
            'newsletter_paginator': newsletter_page_obj,
            'user': self.request.user
        }
        return render(self.request, self.template_name, context)

logger = logging.getLogger(__name__)
class EditarMensagemView(LoginRequiredMixin, UpdateView):
    model = Mensagem
    fields = ['nome', 'email', 'telefone', 'mensagem']
    template_name = 'webiel/pages/mensagens_newsletter.html'
    success_url = reverse_lazy('webiel:mensagens_newsletter')
    
logger = logging.getLogger(__name__)
class DeletarMensagemView(LoginRequiredMixin, DeleteView):
    model = Mensagem
    template_name = 'webiel/pages/mensagens_newsletter.html'
    success_url = reverse_lazy('webiel:mensagens_newsletter')

logger = logging.getLogger(__name__)
class EditarNewsletterView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    fields = ['email']
    template_name = 'webiel/pages/mensagens_newsletter.html'
    success_url = reverse_lazy('webiel:mensagens_newsletter')

logger = logging.getLogger(__name__)
class DeletarNewsletterView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    template_name = 'webiel/pages/  mensagens_newsletter.html'
    success_url = reverse_lazy('webiel:mensagens_newsletter')

logger = logging.getLogger(__name__)
class CartasRecebidasView(LoginRequiredMixin, TemplateView):
    template_name = 'webiel/pages/cartas_recebidas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cartas = CartaRecebida.objects.all().order_by('-data_recepcao')
        
        # Aplicar filtros
        tipo = self.request.GET.get('tipo')
        referencia = self.request.GET.get('referencia')
        if tipo:
            cartas = cartas.filter(tipo=tipo)
        if referencia:
            cartas = cartas.filter(referencia__icontains=referencia)
        
        paginator = Paginator(cartas, 10)  # 10 cartas por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['cartas'] = page_obj.object_list
        context['page_obj'] = page_obj
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                cartas = CartaRecebida.objects.all().order_by('-data_recepcao')
                tipo = request.GET.get('tipo')
                referencia = request.GET.get('referencia')
                if tipo:
                    cartas = cartas.filter(tipo=tipo)
                if referencia:
                    cartas = cartas.filter(referencia__icontains=referencia)
                
                response_data = {
                    'success': True,
                    'cartas': [{
                        'id': carta.id,
                        'tipo': carta.tipo,
                        'get_tipo_display': carta.get_tipo_display(),
                        'nome': carta.nome,
                        'referencia': carta.referencia,
                        'data_recepcao': carta.data_recepcao.strftime('%d/%m/%Y %H:%M'),
                        'autor_recepcao': carta.autor_recepcao.username if carta.autor_recepcao else 'Não definido',
                        'objetivo': carta.objetivo
                    } for carta in cartas]
                }
                logger.debug(f"Resposta JSON (filtro): {response_data}")
                return JsonResponse(response_data)
            except Exception as e:
                logger.error(f"Erro ao processar requisição AJAX: {str(e)}")
                return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            tipo = data.get('tipo')
            nome = data.get('nome')
            referencia = data.get('referencia')
            objetivo = data.get('objetivo')

            if not all([tipo, nome, objetivo]):
                logger.error("Campos obrigatórios ausentes.")
                return JsonResponse({'success': False, 'message': 'Os campos tipo, nome e objetivo são obrigatórios.'}, status=400)

            if tipo not in ['transferencia', 'recomendacao', 'convite', 'outros']:
                logger.error(f"Tipo de carta inválido: {tipo}")
                return JsonResponse({'success': False, 'message': 'Tipo de carta inválido.'}, status=400)

            carta = CartaRecebida(
                tipo=tipo,
                nome=nome,
                referencia=referencia,
                objetivo=objetivo,
                autor_recepcao=request.user
            )
            carta.save()

            response_data = {
                'success': True,
                'message': 'Carta registrada com sucesso!',
                'carta': {
                    'id': carta.id,
                    'tipo': carta.tipo,
                    'get_tipo_display': carta.get_tipo_display(),
                    'nome': carta.nome,
                    'referencia': carta.referencia,
                    'data_recepcao': carta.data_recepcao.strftime('%d/%m/%Y %H:%M'),
                    'autor_recepcao': carta.autor_recepcao.username if carta.autor_recepcao else 'Não definido',
                    'objetivo': carta.objetivo
                }
            }
            logger.debug(f"Carta registrada: {response_data}")
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            logger.error("Erro ao processar JSON.")
            return JsonResponse({'success': False, 'message': 'Erro ao processar os dados.'}, status=400)
        except Exception as e:
            logger.error(f"Erro interno: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

@require_GET
def carta_detalhes(request):
    try:
        carta_id = request.GET.get('id')
        if not carta_id:
            logger.error("ID da carta não fornecido.")
            return JsonResponse({'success': False, 'message': 'ID da carta não fornecido.'}, status=400)
        
        carta = CartaRecebida.objects.get(id=carta_id)
        response_data = {
            'success': True,
            'carta': {
                'id': carta.id,
                'tipo': carta.tipo,
                'get_tipo_display': carta.get_tipo_display(),
                'nome': carta.nome,
                'referencia': carta.referencia,
                'data_recepcao': carta.data_recepcao.strftime('%d/%m/%Y %H:%M'),
                'autor_recepcao': carta.autor_recepcao.username if carta.autor_recepcao else 'Não definido',
                'objetivo': carta.objetivo
            }
        }
        logger.debug(f"Detalhes da carta {carta_id}: {response_data}")
        return JsonResponse(response_data)
    except CartaRecebida.DoesNotExist:
        logger.error(f"Carta {carta_id} não encontrada.")
        return JsonResponse({'success': False, 'message': 'Carta não encontrada.'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao buscar detalhes da carta {carta_id}: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

@require_POST
def carta_editar(request):
    try:
        data = json.loads(request.body)
        carta_id = data.get('carta_id')
        tipo = data.get('tipo')
        nome = data.get('nome')
        referencia = data.get('referencia')
        objetivo = data.get('objetivo')

        if not all([carta_id, tipo, nome, objetivo]):
            logger.error("Campos obrigatórios ausentes na edição.")
            return JsonResponse({'success': False, 'message': 'Os campos carta_id, tipo, nome e objetivo são obrigatórios.'}, status=400)

        if tipo not in ['transferencia', 'recomendacao', 'convite', 'outros']:
            logger.error(f"Tipo de carta inválido: {tipo}")
            return JsonResponse({'success': False, 'message': 'Tipo de carta inválido.'}, status=400)

        carta = CartaRecebida.objects.get(id=carta_id)
        carta.tipo = tipo
        carta.nome = nome
        carta.referencia = referencia
        carta.objetivo = objetivo
        carta.save()

        response_data = {
            'success': True,
            'message': 'Carta actualizada com sucesso!',
            'carta': {
                'id': carta.id,
                'tipo': carta.tipo,
                'get_tipo_display': carta.get_tipo_display(),
                'nome': carta.nome,
                'referencia': carta.referencia,
                'data_recepcao': carta.data_recepcao.strftime('%d/%m/%Y %H:%M'),
                'autor_recepcao': carta.autor_recepcao.username if carta.autor_recepcao else 'Não definido',
                'objetivo': carta.objetivo
            }
        }
        logger.debug(f"Carta {carta_id} atualizada: {response_data}")
        return JsonResponse(response_data)
    except CartaRecebida.DoesNotExist:
        logger.error(f"Carta {carta_id} não encontrada na edição.")
        return JsonResponse({'success': False, 'message': 'Carta não encontrada.'}, status=404)
    except Exception as e:
        logger.error(f"Erro interno na edição: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

@require_POST
def carta_deletar(request):
    try:
        data = json.loads(request.body)
        carta_id = data.get('carta_id')
        if not carta_id:
            logger.error("ID da carta não fornecido na exclusão.")
            return JsonResponse({'success': False, 'message': 'ID da carta não fornecido.'}, status=400)

        carta = CartaRecebida.objects.get(id=carta_id)
        carta.delete()
        logger.debug(f"Carta {carta_id} excluída com sucesso.")
        return JsonResponse({'success': True, 'message': 'Carta excluída com sucesso!'})
    except CartaRecebida.DoesNotExist:
        logger.error(f"Carta {carta_id} não encontrada na exclusão.")
        return JsonResponse({'success': False, 'message': 'Carta não encontrada.'}, status=404)
    except Exception as e:
        logger.error(f"Erro interno na exclusão: {str(e)}")
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

logger = logging.getLogger(__name__)
class InscricoesView(LoginRequiredMixin, TemplateView):
    template_name = 'webiel/pages/inscricoes.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            inscricoes = Inscricao.objects.all().order_by('-data_criacao')
            
            # Aplicar filtros
            departamento_id = self.request.GET.get('departamento')
            atividade_id = self.request.GET.get('atividade')
            if departamento_id:
                inscricoes = inscricoes.filter(departamento_id=departamento_id)
            if atividade_id:
                inscricoes = inscricoes.filter(atividade_id=atividade_id)
            
            paginator = Paginator(inscricoes, 10)  # 10 inscrições por página
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['inscricoes'] = page_obj.object_list
            context['page_obj'] = page_obj
            context['atividades'] = Atividade.objects.filter(disponivel=True)
            context['departamentos'] = Department.objects.all()
            return context
        except Exception as e:
            logger.error(f"Erro em get_context_data: {str(e)}")
            raise ValueError(f"Erro ao preparar contexto: {str(e)}")

    def get(self, request, *args, **kwargs):
        logger.debug(f"Requisição recebida: AJAX={request.headers.get('X-Requested-With')}, GET params={request.GET}")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                inscricoes = Inscricao.objects.all().order_by('-data_criacao')
                departamento_id = request.GET.get('departamento')
                atividade_id = request.GET.get('atividade')
                if departamento_id:
                    inscricoes = inscricoes.filter(departamento_id=departamento_id)
                if atividade_id:
                    inscricoes = inscricoes.filter(atividade_id=atividade_id)
                
                # Calcular o somatório total
                total_valor = inscricoes.aggregate(total_valor=Sum('total'))['total_valor'] or 0.00
                
                response_data = {
                    'success': True,
                    'inscricoes': [{
                        'id': inscricao.id,
                        'nome_completo': inscricao.nome_completo,
                        'atividade': inscricao.atividade.nome,
                        'atividade_id': inscricao.atividade.id,
                        'departamento': inscricao.departamento.name,
                        'departamento_id': inscricao.departamento.id,
                        'email': inscricao.email,
                        'telefone': inscricao.telefone,
                        'data_criacao': inscricao.data_criacao.strftime('%d/%m/%Y %H:%M'),
                        'total': float(inscricao.total or 0),  # Incluir o campo total
                        'preco': float(inscricao.atividade.preco or 0),
                        'pago': inscricao.pago
                    } for inscricao in inscricoes],
                    'total_valor': float(total_valor)  # Incluir o somatório
                }
                logger.debug(f"Resposta JSON: {response_data}")
                return JsonResponse(response_data)
            except Exception as e:
                logger.error(f"Erro ao processar requisição AJAX: {str(e)}")
                return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)
        return super().get(request, *args, **kwargs)

@require_GET
def inscricao_detalhes(request):
    try:
        inscricao_id = request.GET.get('id')
        if not inscricao_id:
            return JsonResponse({'success': False, 'message': 'ID da inscrição não fornecido.'}, status=400)
        
        inscricao = Inscricao.objects.get(id=inscricao_id)
        return JsonResponse({
            'success': True,
            'inscricao': {
                'id': inscricao.id,
                'atividade_id': inscricao.atividade.id,
                'atividade': inscricao.atividade.nome,
                'departamento_id': inscricao.departamento.id,
                'departamento': inscricao.departamento.name,
                'nome_completo': inscricao.nome_completo,
                'email': inscricao.email,
                'telefone': inscricao.telefone,
                'data_nascimento': inscricao.data_nascimento.strftime('%Y-%m-%d'),
                'emergencia_nome1': inscricao.emergencia_nome1,
                'emergencia_telefone1': inscricao.emergencia_telefone1,
                'emergencia_nome2': inscricao.emergencia_nome2,
                'emergencia_telefone2': inscricao.emergencia_telefone2,
                'observacoes': inscricao.observacoes,
                'metodo_pagamento': inscricao.metodo_pagamento,
                'get_metodo_pagamento_display': inscricao.get_metodo_pagamento_display(),
                'valor_entrada': str(inscricao.valor_entrada) if inscricao.valor_entrada else None,
                'valor_transferencia': str(inscricao.valor_transferencia) if inscricao.valor_transferencia else None,
                'comprovativo_transferencia': inscricao.comprovativo_transferencia.url if inscricao.comprovativo_transferencia else None,
                'referencia_pagamento': inscricao.referencia_pagamento,
                'total': str(inscricao.total) if inscricao.total else None,
                'pago': inscricao.pago,
                'data_criacao': inscricao.data_criacao.strftime('%d/%m/%Y %H:%M')
            }
        })
    except Inscricao.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Inscrição não encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

@require_POST
def inscricao_editar(request):
    try:
        form_data = request.POST
        files = request.FILES

        inscricao_id = form_data.get('inscricao_id')
        if not inscricao_id:
            return JsonResponse({'success': False, 'message': 'ID da inscrição não fornecido.'}, status=400)

        # Validação dos campos obrigatórios
        required_fields = ['atividade', 'departamento', 'nome_completo', 'email', 'telefone', 'data_nascimento', 'metodo_pagamento']
        for field in required_fields:
            if not form_data.get(field):
                return JsonResponse({'success': False, 'message': f'O campo {field} é obrigatório.'}, status=400)

        # Validar atividade e departamento
        atividade_id = form_data.get('atividade')
        departamento_id = form_data.get('departamento')
        try:
            atividade = Atividade.objects.get(id=atividade_id, disponivel=True)
            departamento = Department.objects.get(id=departamento_id)
        except Atividade.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Atividade inválida ou não disponível.'}, status=400)
        except Department.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Departamento inválido.'}, status=400)

        # Validar restrição de Gala
        if atividade.nome.lower() == 'gala' and departamento.name.lower() != 'adolescentes':
            return JsonResponse({'success': False, 'message': 'A atividade "Gala" é restrita ao departamento "Adolescentes".'}, status=400)

        # Validar data de nascimento
        data_nascimento = form_data.get('data_nascimento')
        try:
            datetime.strptime(data_nascimento, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Data de nascimento inválida.'}, status=400)

        # Validar método de pagamento
        metodo_pagamento = form_data.get('metodo_pagamento')
        if metodo_pagamento not in ['mao', 'transferencia']:
            return JsonResponse({'success': False, 'message': 'Método de pagamento inválido.'}, status=400)

        # Validar valores monetários
        valor_entrada = form_data.get('valor_entrada', '0').replace(',', '.')
        valor_transferencia = form_data.get('valor_transferencia', '0').replace(',', '.')
        try:
            valor_entrada = decimal.Decimal(valor_entrada) if valor_entrada else None
            valor_transferencia = decimal.Decimal(valor_transferencia) if valor_transferencia else None
        except decimal.InvalidOperation:
            return JsonResponse({'success': False, 'message': 'Valores monetários inválidos.'}, status=400)

        # Calcular total
        total = (valor_entrada or 0) + (valor_transferencia or 0)

        # Validar comprovativo
        comprovativo = files.get('comprovativo_transferencia')
        if comprovativo:
            validator = FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])
            validator(comprovativo)

        # Atualizar inscrição
        inscricao = Inscricao.objects.get(id=inscricao_id)
        inscricao.atividade = atividade
        inscricao.departamento = departamento
        inscricao.nome_completo = form_data.get('nome_completo')
        inscricao.email = form_data.get('email')
        inscricao.telefone = form_data.get('telefone')
        inscricao.data_nascimento = data_nascimento
        inscricao.emergencia_nome1 = form_data.get('emergencia_nome1', '')
        inscricao.emergencia_telefone1 = form_data.get('emergencia_telefone1', '')
        inscricao.emergencia_nome2 = form_data.get('emergencia_nome2', '')
        inscricao.emergencia_telefone2 = form_data.get('emergencia_telefone2', '')
        inscricao.observacoes = form_data.get('observacoes', '')
        inscricao.metodo_pagamento = metodo_pagamento
        inscricao.valor_entrada = valor_entrada
        inscricao.valor_transferencia = valor_transferencia
        if comprovativo:
            inscricao.comprovativo_transferencia = comprovativo
        inscricao.total = total
        inscricao.pago = form_data.get('pago') == 'on'
        inscricao.save()

        return JsonResponse({
            'success': True,
            'message': 'Inscrição atualizada com sucesso!',
            'inscricao': {
                'id': inscricao.id,
                'nome_completo': inscricao.nome_completo,
                'atividade': inscricao.atividade.nome,
                'departamento': inscricao.departamento.name,
                'email': inscricao.email,
                'data_criacao': inscricao.data_criacao.strftime('%d/%m/%Y %H:%M'),
                'pago': inscricao.pago
            }
        })
    except Inscricao.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Inscrição não encontrada.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'success': False, 'message': f'Erro de validação: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

@require_POST
def inscricao_deletar(request):
    try:
        data = json.loads(request.body)
        inscricao_id = data.get('inscricao_id')
        if not inscricao_id:
            return JsonResponse({'success': False, 'message': 'ID da inscrição não fornecido.'}, status=400)

        inscricao = Inscricao.objects.get(id=inscricao_id)
        inscricao.delete()
        return JsonResponse({'success': True, 'message': 'Inscrição excluída com sucesso!'})
    except Inscricao.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Inscrição não encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Erro interno: {str(e)}'}, status=500)

def download_inscricoes_pdf(request):
    # Filtrar inscrições
    inscricoes = Inscricao.objects.all().order_by('nome_completo')
    departamento_id = request.GET.get('departamento')
    atividade_id = request.GET.get('atividade')
    title = "Lista de Inscritos"
    subtitle_parts = []

    # Construir título com atividade e departamento
    if atividade_id:
        try:
            atividade = Atividade.objects.get(id=atividade_id)
            subtitle_parts.append(atividade.nome.capitalize())
            inscricoes = inscricoes.filter(atividade_id=atividade_id)
        except Atividade.DoesNotExist:
            logger.error(f"Atividade {atividade_id} não encontrada.")
            subtitle_parts.append("Atividade Inválida")
    if departamento_id:
        try:
            departamento = Department.objects.get(id=departamento_id)
            subtitle_parts.append(departamento.name.capitalize())
            inscricoes = inscricoes.filter(departamento_id=departamento_id)
        except Department.DoesNotExist:
            logger.error(f"Departamento {departamento_id} não encontrado.")
            subtitle_parts.append("Departamento Inválido")

    if subtitle_parts:
        title = f"Lista de Inscrição {' - '.join(subtitle_parts)}"
    else:
        title = "Lista de Inscritos"

    # Configurar o PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.75*inch,
        bottomMargin=0.5*inch
    )
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo do título
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        textColor=colors.darkblue
    )

    # Estilo do subtítulo
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=15,
        fontName='Helvetica',
        textColor=colors.grey
    )

    # Estilo do rodapé
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_RIGHT,
        fontName='Helvetica',
        textColor=colors.grey
    )

    # Estilo para o texto da tabela
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        textColor=colors.black,
        leading=10,
        wordWrap='CJK'  # Permite quebra de texto longo
    )

    # Adicionar título
    elements.append(Paragraph(title, title_style))

    # Adicionar subtítulo com data e hora de geração
    current_datetime = datetime.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f"Gerado em {current_datetime}", subtitle_style))
    elements.append(Spacer(1, 0.25*inch))

    # Dados da tabela
    data = [['Nome Completo', 'Data de Inscrição', 'Idade', 'Referência de Pagamento', 'Valor Pago']]
    for inscricao in inscricoes:
        # Calcular idade
        birth_date = inscricao.data_nascimento
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Formatando o valor pago
        valor_pago = f"{inscricao.total:.2f}" if inscricao.total else "0.00"
        
        # Quebra de texto para nomes longos e referências
        nome_completo = Paragraph(inscricao.nome_completo, table_text_style)
        referencia_pagamento = Paragraph(inscricao.referencia_pagamento or '-', table_text_style)
        
        data.append([
            nome_completo,
            inscricao.data_criacao.strftime('%d/%m/%Y %H:%M'),
            str(age),
            referencia_pagamento,
            valor_pago
        ])

    # Criar tabela com larguras ajustadas
    table = Table(data, colWidths=[2.5*inch, 1.5*inch, 0.7*inch, 1.8*inch, 1.0*inch])
    table.setStyle(TableStyle([
        # Estilo do cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        # Estilo das linhas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        # Linhas alternadas
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Quebra de texto
    ]))
    elements.append(table)

    # Adicionar rodapé em todas as páginas
    def add_footer(canvas, doc):
        canvas.saveState()
        footer_text = "Gerado por IEL - Todos os direitos reservados"
        footer = Paragraph(footer_text, footer_style)
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, 0.3*inch)
        canvas.restoreState()

    # Construir o PDF
    try:
        doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}")
        return HttpResponse("Erro ao gerar o PDF.", status=500)

    buffer.seek(0)
    
    # Configurar resposta
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title.lower().replace(" ", "_")}.pdf"'
    buffer.close()
    return response
    # Filtrar inscrições
    inscricoes = Inscricao.objects.all().order_by('-data_criacao')
    departamento_id = request.GET.get('departamento')
    atividade_id = request.GET.get('atividade')
    title = "Lista de Inscritos"
    subtitle_parts = []

    if atividade_id:
        try:
            atividade = Atividade.objects.get(id=atividade_id)
            subtitle_parts.append(atividade.nome.capitalize())
            inscricoes = inscricoes.filter(atividade_id=atividade_id)
        except Atividade.DoesNotExist:
            logger.error(f"Atividade {atividade_id} não encontrada.")
            subtitle_parts.append("Atividade Inválida")
    if departamento_id:
        try:
            departamento = Department.objects.get(id=departamento_id)
            subtitle_parts.append(departamento.name.capitalize())
            inscricoes = inscricoes.filter(departamento_id=departamento_id)
        except Department.DoesNotExist:
            logger.error(f"Departamento {departamento_id} não encontrado.")
            subtitle_parts.append("Departamento Inválido")

    if subtitle_parts:
        title = f"Lista de Inscrição {' - '.join(subtitle_parts)}"

    # Configurar o PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo do título
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        textColor=colors.darkblue
    )

    # Estilo do subtítulo
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica',
        textColor=colors.grey
    )

    # Estilo do rodapé
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_RIGHT,
        fontName='Helvetica',
        textColor=colors.grey
    )

    # Adicionar título
    elements.append(Paragraph(title, title_style))

    # Adicionar subtítulo com data e hora de geração
    current_datetime = datetime.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f"Gerado em {current_datetime}", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))

    # Dados da tabela
    data = [['Nome Completo', 'Atividade', 'Departamento', 'Data de Inscrição', 'Idade', 'Referência de Pagamento', 'Valor Pago']]
    for inscricao in inscricoes:
        # Calcular idade
        birth_date = inscricao.data_nascimento
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Formatando o valor pago
        valor_pago = f"{inscricao.total:.2f}" if inscricao.total else "0.00"
        
        data.append([
            inscricao.nome_completo,
            inscricao.atividade.nome,
            inscricao.departamento.name,
            inscricao.data_criacao.strftime('%d/%m/%Y %H:%M'),
            str(age),
            inscricao.referencia_pagamento or '-',
            valor_pago
        ])

    # Criar tabela com larguras ajustadas
    table = Table(data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 1.5*inch, 0.8*inch, 1.5*inch, 1.2*inch])
    table.setStyle(TableStyle([
        # Estilo do cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Estilo das linhas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        # Linhas alternadas
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    # Adicionar rodapé em todas as páginas
    def add_footer(canvas, doc):
        canvas.saveState()
        footer_text = "Gerado por IEL - Todos os direitos reservados"
        footer = Paragraph(footer_text, footer_style)
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, 0.3*inch)
        canvas.restoreState()

    # Construir o PDF
    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    buffer.seek(0)
    
    # Configurar resposta
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title.lower().replace(" ", "_")}.pdf"'
    buffer.close()
    return response
    # Filtrar inscrições
    inscricoes = Inscricao.objects.all().order_by('-data_criacao')
    departamento_id = request.GET.get('departamento')
    atividade_id = request.GET.get('atividade')
    title = "Lista de Inscritos"

    if atividade_id:
        try:
            atividade = Atividade.objects.get(id=atividade_id)
            title = f"Lista de Inscrição {atividade.nome.capitalize()}"
            inscricoes = inscricoes.filter(atividade_id=atividade_id)
        except Atividade.DoesNotExist:
            logger.error(f"Atividade {atividade_id} não encontrada.")
            title = "Lista de Inscritos (Atividade Inválida)"
    if departamento_id:
        inscricoes = inscricoes.filter(departamento_id=departamento_id)

    # Configurar o PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo do título
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        textColor=colors.darkblue
    )

    # Estilo do subtítulo
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=20,
        fontName='Helvetica',
        textColor=colors.grey
    )

    # Estilo do rodapé
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_RIGHT,
        fontName='Helvetica',
        textColor=colors.grey
    )

    # Adicionar título
    elements.append(Paragraph(title, title_style))

    # Adicionar subtítulo com data e hora de geração
    current_datetime = datetime.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f"Gerado em {current_datetime}", subtitle_style))
    elements.append(Spacer(1, 0.2*inch))

    # Dados da tabela
    data = [['Nome Completo', 'Data de Inscrição', 'Idade', 'Referência de Pagamento', 'Valor Pago']]
    for inscricao in inscricoes:
        # Calcular idade
        birth_date = inscricao.data_nascimento
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Formatando o valor pago
        valor_pago = f"{inscricao.total:.2f}" if inscricao.total else "0.00"
        
        data.append([
            inscricao.nome_completo,
            inscricao.data_criacao.strftime('%d/%m/%Y %H:%M'),
            str(age),
            inscricao.referencia_pagamento or '-',
            valor_pago
        ])

    # Criar tabela
    table = Table(data, colWidths=[2.5*inch, 1.8*inch, 0.8*inch, 1.5*inch, 1.2*inch])
    table.setStyle(TableStyle([
        # Estilo do cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Estilo das linhas
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        # Linhas alternadas
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)

    # Adicionar rodapé em todas as páginas
    def add_footer(canvas, doc):
        canvas.saveState()
        footer_text = "Gerado por IEL - Todos os direitos reservados"
        footer = Paragraph(footer_text, footer_style)
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, 0.3*inch)
        canvas.restoreState()

    # Construir o PDF
    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    buffer.seek(0)
    
    # Configurar resposta
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title.lower().replace(" ", "_")}.pdf"'
    buffer.close()
    return response