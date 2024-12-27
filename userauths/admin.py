from django.contrib import admin
from userauths.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','primeiro_nome', 'ultimo_nome', 'email', 'bio',]


admin.site.register(User, UserAdmin)
