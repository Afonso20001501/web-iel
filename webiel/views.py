from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'webiel/pages/index.html')

def sobre(request):
    return render(request, 'webiel/pages/sobre_historial.html')

def sobre_missao(request):
    return render(request,  'webiel/pages/sobre_missao.html')

def sobre_estatuto(request):
    return render(request,  'webiel/pages/sobre_estatuto.html')

def sobre_pacto(request):
    return render(request,  'webiel/pages/sobre_pacto.html')

def sobre_fe(request):
    return render(request,  'webiel/pages/sobre_fe.html')

def sobre_pratica(request):
    return render(request,  'webiel/pages/sobre_pratica.html')

def noticia_iel(request):
    return render(request,  'webiel/pages/noticia_iel.html')

def contato(request):
    return render(request,  'webiel/pages/contato.html')

def mocidade(request):
    return render(request,  'webiel/pages/mocidade.html')

def senhoras(request):
    return render(request,  'webiel/pages/senhoras.html')

def devem(request):
    return render(request,  'webiel/pages/devem.html')

def homens(request):
    return render(request,  'webiel/pages/homens.html')

def musica(request):
    return render(request,  'webiel/pages/musica.html')