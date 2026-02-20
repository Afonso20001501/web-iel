
from django.contrib import admin

from webiel import forms
from .models import Adolescentes, Atividade, Category, Department, Devem, Homens, Inscricao, Mocidade, Musica, Noticia, BancoDeAlimentacao, Casamento, Carta, Newsletter, Mensagem, Photo, Senhoras


class PhotoAdmin(admin.ModelAdmin):
    form = forms.PhotoAdminForm
    list_display = ('department', 'upload_date', 'expires_on')
    list_filter = ('department',)
    search_fields = ('department__name', 'description')

    def save_model(self, request, obj, form, change):
        if 'image' in request.FILES:
            images = request.FILES.getlist('image')
            if len(images) > 30:
                self.message_user(request, "Limite de 30 fotos excedido. Apenas as primeiras 30 foram salvas.", level='warning')
                images = images[:30]
            for image in images:
                # Cria uma nova instância de Photo para cada imagem
                photo = Photo(
                    department=obj.department,
                    image=image,
                    description=obj.description
                )
                photo.save()  # Chama o método save do modelo
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Department)
admin.site.register(Photo, PhotoAdmin)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
admin.site.register(Noticia)
admin.site.register(BancoDeAlimentacao)
admin.site.register(Casamento)
admin.site.register(Carta)
admin.site.register(Newsletter)
admin.site.register(Mensagem)
admin.site.register(Mocidade)
admin.site.register(Devem)
admin.site.register(Senhoras)
admin.site.register(Homens)
admin.site.register(Musica)
admin.site.register(Adolescentes)
admin.site.register(Atividade)
admin.site.register(Inscricao)