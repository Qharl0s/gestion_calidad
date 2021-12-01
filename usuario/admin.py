from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Oficina
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'oficina','cNombres', 'cCargo', 'email', 'lRevisor', 'is_staff','is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Suscription dates'), {'fields': ('oficina','cNombres', 'cCargo', 'email', 'lRevisor','is_active', 'is_staff', 'is_superuser')}),
    )
    list_filter = ()

class oficinaAdmin(admin.ModelAdmin):
    list_display = ('id','cOficina')

    def __str__(self):
        return self.oficina.cOficina

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Oficina, oficinaAdmin)
admin.site.unregister(Group)