from decimal import Decimal
import uuid
from django.forms import ValidationError
from django.utils import timezone
import logging
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import timedelta
from base.base import BaseModel
import logging
from django.core.validators import FileExtensionValidator

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
    (5,"Musica"),
    (6,"Adolescentes")
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
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Banco De Alimentação'
    def __str__(self):
        return self.nome

class Casamento(models.Model):
    nome_noivo = models.CharField(max_length=255, null=False)
    nome_noiva = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=65, null=False)
    data_casam = models.DateField(null=False)
    
    class Meta:
        verbose_name_plural = 'Casamentos'
    def __str__(self):
        return self.nome_noivo
logger = logging.getLogger(__name__)

class Carta(models.Model):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=65, null=False)
    destino = models.CharField(max_length=255, null=False)
    objectivo = models.CharField(max_length=255, null=False)
    tipo_carta = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=65, null=False)
    outras_inf = models.TextField(null=False)
    data_solicitacao = models.DateTimeField(auto_now_add=True, null=True)
    foi_feita = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    referencia = models.CharField(max_length=20, unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Cartas'

    def __str__(self):
        return f"{self.nome} - {self.tipo_carta} ({self.referencia})"

    def save(self, *args, **kwargs):
        if not self.referencia:
            # Normalizar tipo_carta para comparação
            tipo_normalizado = self.tipo_carta.strip().lower()
            logger.debug(f"Tipo de carta normalizado: {tipo_normalizado}")
            if 'recomend' in tipo_normalizado:  # Suporta variações como "Recomendação", "recomendacao"
                prefixo = 'REC'
            elif 'transfer' in tipo_normalizado:  # Suporta variações como "Transferência", "transferencia"
                prefixo = 'TRA'
            else:
                logger.error(f"Tipo de carta inválido: {self.tipo_carta}")
                prefixo = 'TRA'  # Padrão para evitar falhas
            ano = self.data_solicitacao.year if self.data_solicitacao else 2026
            count = Carta.objects.filter(
                tipo_carta=self.tipo_carta,
                data_solicitacao__year=ano
            ).count() + 1
            self.referencia = f"{prefixo}{ano}-{count:03d}"
            logger.info(f"Gerada referência: {self.referencia} para carta {self.nome}")
        super().save(*args, **kwargs)

class Mensagem(models.Model):
    nome = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=65, null=False)
    telefone = models.CharField(max_length=65, null=False)
    mensagem = models.TextField(null=False)
    created_at = models.DateTimeField(null=True, blank=True)  # Adicionado para rastrear data de criação


    class Meta:
        verbose_name_plural = 'Mensagens'
    def __str__(self):
        return self.nome

class Newsletter(models.Model):
    email = models.EmailField(max_length=65, null=False) 
    created_at = models.DateTimeField(null=True, blank=True)  # Adicionado para rastrear data de criação

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

class Adolescentes(BaseModel):
   presidente = models.CharField(max_length=100, null=False)
   
   class Meta:
        verbose_name_plural = 'Adolescentes'
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

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Departamentos"

class Photo(models.Model):
    image = models.ImageField(upload_to='noticia/%Y/%m/%d/')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Define expires_on apenas se ainda não estiver definido
        if not self.expires_on:
            # Usa upload_date se disponível, caso contrário usa timezone.now()
            base_date = self.upload_date or timezone.now()
            self.expires_on = base_date + timedelta(days=31)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Foto para {self.department.name} - {self.upload_date}"

    class Meta:
        verbose_name_plural = "Fotos"
        ordering = ['-upload_date']

class CartaRecebida(models.Model):
    TIPO_CHOICES = [
        ('transferencia', 'Transferência'),
        ('recomendacao', 'Recomendação'),
        ('convite', 'Convite'),
        ('outros', 'Outros Documentos'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=255)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    data_recepcao = models.DateTimeField(auto_now_add=True)
    autor_recepcao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    objetivo = models.TextField()

    class Meta:
        verbose_name_plural = 'Cartas Recebidas'
        ordering = ['-data_recepcao']

    def __str__(self):
        return f"{self.nome} - {self.get_tipo_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Atividade(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    emoji = models.CharField(max_length=10, blank=True)
    disponivel = models.BooleanField(default=True)  # Adiciona um campo booleano

    class Meta:
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.nome

class Prestacao(models.Model):
    inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE, related_name='prestacoes')
    numero = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_esperada = models.DateField(null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    pago = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True, null=True) 
    metodo_pagamento = models.CharField(max_length=20, null=True, blank=True, choices=[('mao', 'Dinheiro em Espécie'), ('transferencia', 'Transferência Bancária')]) # Novo campo
    comprovativo = models.FileField(
        upload_to='comprovativos/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])]
    )

    class Meta:
        ordering = ['numero']
        unique_together = ('inscricao', 'numero')

    def __str__(self):
        return f"Prestação {self.numero} - Inscrição {self.inscricao.referencia_pagamento}"

class Inscricao(models.Model):
    METODO_PAGAMENTO_CHOICES = [
        ('mao', 'Dinheiro em espécie'),
        ('transferencia', 'Transferência Bancária'),
    ]
    
    TIPO_PAGAMENTO_CHOICES = [
        ('avista', 'Pagamento à Vista'),
        ('parcelado', 'Pagamento Parcelado'),
    ]

    # Relacionamentos
    atividade = models.ForeignKey(Atividade, on_delete=models.PROTECT, related_name='inscricoes')
    departamento = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='inscricoes')
    
    # Dados pessoais
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField(null=True, blank=True)  # Opcional
    nome_conjuge = models.CharField(max_length=255, blank=True, null=True)  # Para encontros de casais
    
    # Contactos de emergência
    emergencia_nome1 = models.CharField(max_length=255, blank=True, null=True)
    emergencia_telefone1 = models.CharField(max_length=20, blank=True, null=True)
    emergencia_nome2 = models.CharField(max_length=255, blank=True, null=True)
    emergencia_telefone2 = models.CharField(max_length=20, blank=True, null=True)
    
    # Observações
    observacoes = models.TextField(blank=True, null=True)
    
    # Pagamento
    metodo_pagamento = models.CharField(max_length=20, choices=METODO_PAGAMENTO_CHOICES)
    tipo_pagamento = models.CharField(max_length=20, choices=TIPO_PAGAMENTO_CHOICES, default='avista')
    numero_parcelas = models.PositiveIntegerField(default=1)
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_transferencia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comprovativo_transferencia = models.FileField(
        upload_to='comprovativos/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg'])]
    )
    referencia_pagamento = models.CharField(max_length=20, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pago = models.BooleanField(default=False)
    
    # Metadados
    data_criacao = models.DateTimeField(auto_now_add=True, null=True)
    data_atualizacao = models.DateTimeField(auto_now=True, null=True)
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_transferencia = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['pago']),
        ]

    def __str__(self):
        return f'Inscrição #{self.id} - {self.nome_completo}'

    def save(self, *args, **kwargs):
        if not self.referencia_pagamento:
            self.referencia_pagamento = self.gerar_referencia()
        
        # Validação para encontros de casais
        if self.atividade.slug == 'encontros-de-casais' and not self.nome_conjuge:
            raise ValidationError("Nome do cônjuge é obrigatório para encontros de casais")
        
        super().save(*args, **kwargs)
    
    def gerar_referencia(self):
        data = timezone.now().strftime('%Y%m%d')
        ultima_inscricao = Inscricao.objects.filter(
            referencia_pagamento__startswith=f'IEL-{data}'
        ).count()
        return f"IEL-{data}-{ultima_inscricao + 1:04d}"
    
    def calcular_valor_parcela(self):
        if self.tipo_pagamento == 'parcelado' and self.numero_parcelas > 1:
            return self.total / self.numero_parcelas
        return self.total

    def get_valor_pago(self):
        # Para pagamento à vista, usa valor_entrada
        if self.tipo_pagamento == 'avista':
            return self.valor_entrada or Decimal('0.00')
        # Para parcelado, usa valor_transferencia para a primeira prestação + prestações pagas
        valor_prestacoes = sum(p.valor for p in self.prestacoes.filter(pago=True)) or Decimal('0.00')
        return valor_prestacoes

    def get_prestacoes_pendentes(self):
        return self.prestacoes.filter(pago=False).count()