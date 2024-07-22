from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from base.base import BaseModel



# Create your models here.
# Tabelea de Categoria
class Category(models.Model):
    categoria = models.CharField(max_length=20, verbose_name='Categoria')
    class Meta:
        verbose_name_plural = 'Categorias'
    def __str__(self):
        return self.categoria

DEPARTAMENTO = (
    (0,"Mocidade"),
    (1,"Senhoras"),
    (2,"Devem"),
    (3,"Homens"),
    (5,"Musica")
)

CARTAS = (
    (0,"Recomendacão"),
    (1,"Transferência")
)

# Tabela de noticias
class Noticia(models.Model):
    title = models.CharField(max_length=65)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    creted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='noticia/img/%Y/%m/%d/')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    autorCitacao = models.CharField(max_length=65, default='')
    autorCargo = models.CharField(max_length=80, default='')
    citacao = models.TextField(max_length=500, default='')
    dataEvento = models.CharField(max_length=65, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Noticias'
    def __str__(self):
        return self.title
    

class BancoDeAlimentacao(models.Model):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=65, null=False)
    telefone = models.CharField(max_length=65,null=False)
    bairro = models.CharField(max_length=255, null=False)
    donativo = models.TextField(null=False)

    class Meta:
        verbose_name_plural = 'Banco De Alimentação'
    def __str__(self):
        return self.nome

class Casamento(models.Model):
    nome_noivo = models.CharField(max_length=255, null=False)
    nome_noiva = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=65,null=False)
    data_casam = models.DateField(null=False)
    
    class Meta:
        verbose_name_plural = 'Casamentos'
    def __str__(self):
        return self.nome_noivo

class Carta(models.Model):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=65, null=False)
    destino = models.CharField(max_length=255, null=False)
    objectivo = models.CharField(max_length=255, null=False)
    tipo_carta =  models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=65,null=False)
    outras_inf = models.TextField(null=False)
  
    class Meta:
        verbose_name_plural = 'Cartas'
    def __str__(self):
        return self.nome

class Mensagem(models.Model):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=65, null=False)
    telefone = models.CharField(max_length=65,null=False)
    mensagem = models.TextField(null=False)

    class Meta:
        verbose_name_plural = 'Mensagens'
    def __str__(self):
        return self.nome

class Newsletter(models.Model):
    email = models.EmailField(max_length=65, null=False) 

    class Meta:
        verbose_name_plural = 'Newsletter'
    def __str__(self):
        return self.email
    

class Mocidade(BaseModel):
   presidente = models.CharField(max_length=100, null=False)
   
   class Meta:
        verbose_name_plural = 'Mocidade'
   def __str__(self):
        return self.atividade


class Devem(BaseModel):
   presidente = models.CharField(max_length=100, null=False)
   
   class Meta:
        verbose_name_plural = 'Devem'
   def __str__(self):
        return self.atividade


class Musica(BaseModel):
   presidente = models.CharField(max_length=100, null=False)
   
   class Meta:
        verbose_name_plural = 'Musica'
   def __str__(self):
       return self.atividade
   
class Senhoras(BaseModel):
   presidente = models.CharField(max_length=100, null=False)
   
   class Meta:
        verbose_name_plural = 'Senhoras'
   def __str__(self):
        return self.atividade
   

class Homens(BaseModel):
   presidente = models.CharField(max_length=100, null=False)
   
   class Meta:
        verbose_name_plural = 'Homens'
   def __str__(self):
        return self.atividade