from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import Noticia
from .forms import BancoForm, CasaForm, CartForm, NewsForm, MensForm
from django.contrib import messages
from django.core.paginator import Paginator
  
# Create your views here.
def home(request):
    noticias = Noticia.objects.filter(is_published=True).order_by('-id')
    paginator = Paginator(noticias, 3)

   
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

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
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()
        
        else:
            messages.error(request, 'Houve um erro ao salvar o formulário. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        casa_form = CasaForm()
        carta_form = CartForm()
        news_form = NewsForm()

        
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'webiel/pages/index.html', context={
        'noticias': noticias,
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'casa_form': casa_form,
        'carta_form': carta_form,
        'news_form': news_form,
        'page_obj':page_obj,
    })

def noticia_view(request, slug):
    noticia =  get_object_or_404(Noticia, slug=slug, is_published=True)

    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')
    
    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()


    return render(request, 'webiel/pages/noticia-view.html', context={
        'noticia': noticia,
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
      
    })

def sobre(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()

    return render(request, 'webiel/pages/sobre_historial.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def sobre_missao(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()

    return render(request,  'webiel/pages/sobre_missao.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def sobre_estatuto(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()

    return render(request,  'webiel/pages/sobre_estatuto.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def sobre_pacto(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/sobre_pacto.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def sobre_fe(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/sobre_fe.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def sobre_pratica(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()

    return render(request,  'webiel/pages/sobre_pratica.html',  context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def noticia_iel(request):
    noticias = Noticia.objects.filter(is_published=True).order_by('-id').order_by('-id')
    paginator = Paginator(noticias, 3)

    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,  'webiel/pages/noticia_iel.html',context={
        'noticias': noticias,
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
        'page_obj':page_obj,
    })

def contato(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')
    
    if request.method == 'POST':
        mens_form = MensForm(request.POST)
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        if mens_form.is_valid():
            messages.success(request, 'A sua mensagem foi enviada com sucesso!', extra_tags='contact')
            mens_form.save()
        
        elif banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        mens_form = MensForm()
        banco_form = BancoForm()
        news_form = NewsForm()

    return render(request,  'webiel/pages/contato.html', context={
        'noticias_recentes': noticias_recentes,
        'mens_form': mens_form,
        'banco_form': banco_form,
        'news_form': news_form,
    
    })

def mocidade(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/mocidade.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def senhoras(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/senhoras.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def devem(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/devem.html', context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def homens(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/homens.html',context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })

def musica(request):
    noticias_recentes = Noticia.objects.filter(is_published=True).order_by('-id')

    if request.method == 'POST':
        banco_form = BancoForm(request.POST)
        news_form = NewsForm(request.POST)
       
        
        if banco_form.is_valid():
           messages.success(request, 'O seu donativo foi enviado com sucesso!',  extra_tags='banco')
           banco_form.save()
        
        elif news_form.is_valid():
            messages.success(request, 'Enviado com sucesso!', extra_tags='news')
            news_form.save()

        else:
            messages.error(request, 'Houve um erro ao enviar a mensagem. Por favor, verifique os dados e tente novamente.')
    else:
        banco_form = BancoForm()
        news_form = NewsForm()
    return render(request,  'webiel/pages/musica.html',context={
        'noticias_recentes': noticias_recentes,
        'banco_form': banco_form,
        'news_form': news_form,
    })