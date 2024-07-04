from django.contrib import admin
from .models import Category, Noticia, BancoDeAlimentacao, Casamento, Carta, Newsletter, Mensagem

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