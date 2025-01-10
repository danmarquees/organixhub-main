from django.contrib import admin
from userauths.models import User, Profile, Contato

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','primeiro_nome', 'ultimo_nome', 'email', 'bio',]


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'nome','imagem', 'bio', 'telefone', 'verificado',]


class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome','email', 'telefone', 'assunto', 'mensagem',]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contato, ContatoAdmin)
