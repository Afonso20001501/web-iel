from django.contrib import admin
from .models import Category, Devem, Homens, Mocidade, Musica, Noticia, BancoDeAlimentacao, Casamento, Carta, Newsletter, Mensagem, Senhoras

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