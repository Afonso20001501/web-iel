from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Casamento, Carta, Mensagem, BancoDeAlimentacao, Newsletter

  
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