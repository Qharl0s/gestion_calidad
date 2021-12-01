from django.contrib import admin
from .models import Categoria, Grupo, Indicador, MedioVerificacion

class categoriaAdmin(admin.ModelAdmin):
    list_display = ('id','cCategoria')

    def __str__(self):
        return self.categoria
    
class grupoAdmin(admin.ModelAdmin):
    list_display = ('id','cGrupo')

    def __str__(self):
        return self.grupo

class indicadorAdmin(admin.ModelAdmin):
    list_display = ('id','cIndicador')

    def __str__(self):
        return self.indicador

class medioVerificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_indicador', 'cMedioVerificacion', 'get_oficina', 'lVigente', 'nOrden', 'idEstado')
    
    def get_indicador(self, obj):
        return "Indicador %s" % obj.indicador.id
    get_indicador.short_description = 'Indicador'
    get_indicador.admin_order_field = 'medioverificacion__oficina'
    
    def get_oficina(self, obj):
        return obj.oficinaResponsable.cOficina
    get_oficina.short_description = 'Oficina'
    get_oficina.admin_order_field = 'medioverificacion.oficinaResponsable'

admin.site.register(Categoria, categoriaAdmin)
admin.site.register(Grupo, grupoAdmin)
admin.site.register(Indicador, indicadorAdmin)
admin.site.register(MedioVerificacion, medioVerificacionAdmin)