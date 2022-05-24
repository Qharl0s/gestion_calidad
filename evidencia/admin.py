from django.contrib import admin
from .models import Categoria, Evidencia, Evidencia_Todo, Grupo, Indicador, MedioVerificacion

class categoriaAdmin(admin.ModelAdmin):
    list_display = ('id','cCategoria')

    def __str__(self):
        return self.categoria
    
class grupoAdmin(admin.ModelAdmin):
    list_display = ('id','cGrupo')

    def __str__(self):
        return self.grupo

class indicadorAdmin(admin.ModelAdmin):
    list_display = ('cTitulo','cIndicador')

class medioVerificacionAdmin(admin.ModelAdmin):
    list_display = ('cTitulo', 'cMedioVerificacion', 'get_indicador', 'get_oficina', 'lVigente', 'nOrden')
    
    def get_indicador(self, obj):
        return obj.indicador.cTitulo
    get_indicador.short_description = 'Indicador'
    
    def get_oficina(self, obj):
        if obj.oficinaResponsable == None:
            return '-'
        else:
            return obj.oficinaResponsable.cOficina
    get_oficina.short_description = 'Oficina'
    
class evidenciaAdmin(admin.ModelAdmin):
    # list_display = ('id',)
    list_display = ('get_id', 'get_oficina', 'get_medio', 'dFechaCarga', 'lRevisado')
    
    def get_id(self, obj):
        return 'Evd. %s' % (obj.id)
    get_id.short_description = 'ID'
        
    def get_oficina(self, obj):
        if obj.oficina == None:
            return '-'
        else:
            return obj.oficina.cOficina
    get_oficina.short_description = 'Oficina'
    
    def get_medio(self, obj):
        if obj.medioVerificacion == None:
            return '-'
        else:
            return obj.medioVerificacion.cTitulo
    get_medio.short_description = 'Medio Verficacion'
    
class evidenciatodoAdmin(admin.ModelAdmin):
    # list_display = ('id',)
    list_display = ('get_id', 'get_oficina', 'get_medio', 'dFechaCarga', 'lRevisado')
    
    def get_id(self, obj):
        return 'Evd. %s' % (obj.id)
    get_id.short_description = 'ID'
        
    def get_oficina(self, obj):
        if obj.oficina == None:
            return '-'
        else:
            return obj.oficina.cOficina
    get_oficina.short_description = 'Oficina'
    
    def get_medio(self, obj):
        if obj.medioVerificacion == None:
            return '-'
        else:
            return obj.medioVerificacion.cTitulo
    get_medio.short_description = 'Medio Verficacion'

admin.site.register(Categoria, categoriaAdmin)
admin.site.register(Grupo, grupoAdmin)
admin.site.register(Indicador, indicadorAdmin)
admin.site.register(MedioVerificacion, medioVerificacionAdmin)
admin.site.register(Evidencia, evidenciaAdmin)
admin.site.register(Evidencia_Todo, evidenciatodoAdmin)