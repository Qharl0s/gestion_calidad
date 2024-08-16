from evidencia.models import Categoria, Grupo, Indicador, MedioVerificacion

class datos_object(object):
    items = 0
    asignados = 0
    aprobados = 0
    observados = 0
    pendientes = 0
    archivos = 0
    detalles = 0
    revisiones = 0
    se_edita = 0

class objeto(object):
  id = 0
  descripcion = ''
  datos_objeto = datos_object()


def datos_objeto(categoria_id=0, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=0, 
                  oficina_id=0, es_estandar=0, es_revisor=0):
    medios = MedioVerificacion.objects.all()
    #Categoria
    if categoria_id>0:
        medios = medios.filter(indicador__grupo__categoria__id=categoria_id)
    #Grupo
    if grupo_id>0:
        medios = medios.filter(indicador__grupo__id=grupo_id)
    #Indicador
    if indicador_id>0:
        medios = medios.filter(indicador__id=indicador_id)
    #Medio verificacion
    if medio_id>0:
        medios = medios.get(id=medio_id)
    
    objeto = datos_object()
    objeto.items = 1 if medio_id>0 else medios.count()
    #Asignados todo para Estandar y Revisor, si no por oficinaResponsable
    objeto.asignados = 1 if medio_id>0 else medios.count()
    if es_estandar==0 and not es_revisor:
        if medio_id>0:
            objeto.asignados = 1 if medios.oficinaResponsable_id==oficina_id else 0
            objeto.se_edita = 1 if medios.oficinaResponsable_id==oficina_id else 0
        else:
            objeto.asignados = medios.filter(oficinaResponsable_id=oficina_id).count()

    #si no es nivel MedioVerificacion
    if medio_id==0:
        for medio in medios:
            evidencia = medio.evidencia_set.filter(periodo__id=periodo_id, lFinalizado=False)
            if es_estandar==1 or not es_revisor:
                evidencia = evidencia.filter(oficina__id=oficina_id)

            objeto.aprobados += evidencia.filter(idEstado='Aprobado').count()
            objeto.observados += evidencia.filter(idEstado='Observado').count()
        objeto.pendientes += (objeto.asignados - objeto.aprobados - objeto.observados)
    # si es nivel de MedioVerificacion se lee los detalles, archivos y aprobaciones
    if medio_id>0:
        evidencia = medios.evidencia_set.filter(periodo__id=periodo_id)
        if es_estandar==1:
            evidencia = evidencia.filter(lFinalizado=False, oficina__id=oficina_id)

        objeto.aprobados += evidencia.filter(idEstado='Aprobado').count()
        objeto.observados += evidencia.filter(idEstado='Observado').count()
        objeto.pendientes += (objeto.items - objeto.aprobados - objeto.observados)
        if evidencia.count()>0:
            #detalles
            if evidencia.first().cDetalle1 != '':
                objeto.detalles += 1
            if evidencia.first().cDetalle2 != '':
                objeto.detalles += 1
            #archivos
            objeto.archivos = evidencia.first().archivo_set.all().count()
            #revisiones
            objeto.revisiones = evidencia.first().revision_set.all().count()

    return objeto

def listar_objetos(categoria_id=0, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=0, oficina_id=0, es_estandar=0, es_revisor=0):
    objetos = []
    if categoria_id>0 and grupo_id>0 and indicador_id>0 and medio_id>0:
        objetos = lista_categorias(periodo_id, oficina_id, es_estandar, es_revisor)
    elif categoria_id>0:
        objetos = lista_grupos(categoria_id, periodo_id, oficina_id, es_estandar, es_revisor)
    elif grupo_id>0:
        objetos = lista_indicadores(grupo_id, periodo_id, oficina_id, es_estandar, es_revisor)
    elif indicador_id>0:
        objetos = lista_medios(indicador_id, periodo_id, oficina_id, es_estandar, es_revisor)

    return objetos

def lista_categorias(periodo_id, oficina_id, es_estandar, usuario):
    return []

def lista_grupos(categoria_id, periodo_id, oficina_id, es_estandar, es_revisor):
    objetos = []
    grupos = Grupo.objects.filter(categoria__id=categoria_id)
    for grupo in grupos:
        obj = objeto()
        obj.id = grupo.id
        obj.descripcion = grupo.cGrupo
        obj.datos_objeto = datos_objeto(categoria_id, grupo.id, 0, 0, periodo_id, oficina_id, es_estandar, es_revisor)
        objetos.append(obj)
    return objetos

def lista_indicadores(grupo_id, periodo_id, oficina_id, es_estandar, es_revisor):
    objetos = []
    indicadores = Indicador.objects.filter(grupo__id=grupo_id)
    for indicador in indicadores:
        obj = objeto()
        obj.id = indicador.id
        obj.descripcion = indicador.cIndicador
        obj.datos_objeto = datos_objeto(0, 0, indicador.id, 0, periodo_id, oficina_id, es_estandar, es_revisor)
        objetos.append(obj)
    return objetos

def lista_medios(indicador_id, periodo_id, oficina_id, es_estandar, es_revisor):
    objetos = []
    medios = MedioVerificacion.objects.filter(indicador__id=indicador_id)
    for medio in medios:
        obj = objeto()
        obj.id = medio.id
        obj.descripcion = medio.cMedioVerificacion
        obj.datos_objeto = datos_objeto(0, 0, 0, medio.id, periodo_id, oficina_id, es_estandar, es_revisor)
        objetos.append(obj)
    return objetos


def nombre_grupo_func(grupo, tipo):
    id=0
    if tipo==1:
        id = grupo.categoria_id
    elif tipo==2:
        id = grupo.grupo.categoria_id

    if id==1:
        return 'condiciones'
    elif id==2:
        return 'requerimientos'
    elif id==3:
        return 'recomendaciones'
    elif id==4:
        return 'estandares'
    elif id==5:
        return 'renovaciones'
    else:
        return 'Otro Grupo'
    
