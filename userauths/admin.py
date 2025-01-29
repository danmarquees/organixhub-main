from django.contrib import admin
from userauths.models import User, Profile, Contato, Vendedor

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','primeiro_nome', 'ultimo_nome', 'email', 'bio',]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nome','imagem', 'bio', 'telefone', 'verificado', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep']


class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome','email', 'telefone', 'assunto', 'mensagem',]

class VendedorAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf_cnpj', 'email', 'nome_loja', 'categoria_produtos']



admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contato, ContatoAdmin)
admin.site.register(Vendedor, VendedorAdmin)
