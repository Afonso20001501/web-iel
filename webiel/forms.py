from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Casamento, Carta, Mensagem, BancoDeAlimentacao, Newsletter, Noticia, Photo
from django.forms.widgets import FileInput
  
class BancoForm(forms.ModelForm):
    class Meta:
        model = BancoDeAlimentacao
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

class NewsForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

class CasaForm(forms.ModelForm):
    class Meta:
        
        model = Casamento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

class MensForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

class CartForm(forms.ModelForm):
    class Meta:
        model = Carta
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Enviar'))

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = [
            'title', 'category', 'description', 'cover',
            'dataEvento', 'autorCitacao', 'autorCargo', 'citacao', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da publicação',
                'required': 'required'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a descrição da publicação',
                'rows': 5,
                'required': 'required'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'dataEvento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 31/12/2025',
            }),
            'autorCitacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do autor da citação',
            }),
            'autorCargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo do autor',
            }),
            'citacao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite a citação', 
                'rows': 4,
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'title': 'Título',
            'category': 'Categoria',
            'description': 'Descrição',
            'cover': 'Imagem de Capa',
            'dataEvento': 'Data do Evento',
            'autorCitacao': 'Autor da Citação',
            'autorCargo': 'Cargo do Autor',
            'citacao': 'Citação',
            'is_published': 'Publicar imediatamente',
        }

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        exclude = ['author', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
            'dataEvento': forms.TextInput(attrs={'class': 'form-control'}),
            'autorCitacao': forms.TextInput(attrs={'class': 'form-control'}),
            'autorCargo': forms.TextInput(attrs={'class': 'form-control'}),
            'citacao': forms.Textarea(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class MultipleFileInput(FileInput):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.attrs['multiple'] = 'multiple'

class PhotoAdminForm(forms.ModelForm):
    image = forms.FileField(widget=MultipleFileInput(), label="Imagens (máximo 30)")

    class Meta:
        model = Photo
        fields = ['department', 'image', 'description']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'department', 'description']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descreva a foto (opcional)', 'rows': 4}),
        }
        labels = {
            'image': 'Imagem',
            'department': 'Departamento',
            'description': 'Descrição',
        }