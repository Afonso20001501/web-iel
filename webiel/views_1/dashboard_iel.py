from urllib import request
from django.views import View
from webiel.forms import BancoForm, CartForm, CasaForm, NewsForm
from webiel.models import Noticia
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.generic import TemplateView, DetailView

class Home(TemplateView):
    template_name = 'webiel/pages/index.html'

    def get_home(self, request, **kwargs):
        context = super().get_home(request, **kwargs)
        noticias = Noticia.objects.filter(is_published=True).order_by('-id')
        paginator = Paginator(noticias, 3)
        noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')  
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context.update({
            'noticias': noticias,
            'noticias_recentes': noticias_recentes,
            'banco_form': BancoForm(),
            'casa_form': CasaForm(),
            'carta_form': CartForm(),
            'news_form': NewsForm(),
            'page_obj':page_obj,
        })
        
        return  context
            
    def post(self, request, *args, **kwargs):
    
        if request.method == 'POST':
            banco_form = BancoForm(request.POST)
            casa_form = CasaForm(request.POST)
            carta_form = CartForm(request.POST)
            news_form = NewsForm(request.POST)

            if banco_form.is_valid():
                messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
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