from django.contrib import admin
from .models import Periodo, Categoria, Evidencia, Evidencia_Todo, Grupo, Indicador, MedioVerificacion, Archivo, Revision

class periodoAdmin(admin.ModelAdmin):
    list_display = ('cPeriodo', 'categoria', 'lVigente')

    def __str__(self):
        return self.periodo

class categoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cCategoria', 'lVigente')

    def __str__(self):
        return self.categoria
    
class grupoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cGrupo', 'categoria', 'lVigente')

    def __str__(self):
        return self.grupo

class indicadorAdmin(admin.ModelAdmin):
    list_display = ('id', 'cTitulo','cIndicador', 'grupo')

class medioVerificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cTitulo', 'cMedioVerificacion', 'get_indicador', 'get_oficina', 'lVigente', 'nOrden')
    
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
    list_display = ('get_medio', 'periodo', 'get_oficina', 'idEscala', 'dFechaCarga', 'lFinalizado')
    
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
            return obj.medioVerificacion.cMedioVerificacion
    get_medio.short_description = 'Medio Verficacion'
    
class evidenciatodoAdmin(admin.ModelAdmin):
    # list_display = ('id',)
    list_display = ('get_id', 'get_oficina', 'get_medio', 'dFechaCarga')
    
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

class archivoAdmin(admin.ModelAdmin):
    def nombre(self, obj):
        return obj.archivoPdf.name
    
    def periodo(self, obj):
        return obj.evidencia.periodo.cPeriodo
    
    list_display = ('nombre', 'archivoPdf', 'periodo', 'evidencia', 'lVigente')

    def __str__(self):
        return self.archivoPdf
    
class revisionAdmin(admin.ModelAdmin):
    list_display = ('evidencia', 'cRevision', 'idEstado', 'get_ususario', 'dFecha', 'lVigente')
    def get_ususario(self, obj):
        return obj.usuario.username

admin.site.register(Periodo, periodoAdmin)
admin.site.register(Categoria, categoriaAdmin)
admin.site.register(Grupo, grupoAdmin)
admin.site.register(Indicador, indicadorAdmin)
admin.site.register(MedioVerificacion, medioVerificacionAdmin)
admin.site.register(Evidencia, evidenciaAdmin)
admin.site.register(Evidencia_Todo, evidenciatodoAdmin)
admin.site.register(Archivo, archivoAdmin)
admin.site.register(Revision, revisionAdmin)