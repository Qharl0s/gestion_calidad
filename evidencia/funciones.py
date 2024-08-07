class grupo_resumen(object):
  grupo = ''
  grupo2 = ''
  id = 0
  cargados = 0
  aprobados = 0
  observados = 0
  pendientes = 0
  items = 0
  archivos = 0
  detalles = 0
  revisiones = 0
  lEdita = 0

class resumen(object):
  grupos = []
  items = 0

def resumen_grupos(categorias, periodo, oficina, usuario):
    grupos = categorias.first().grupo_set.all()
    resumen_obj = resumen()
    resumen_obj.grupos = []
    for grupo in grupos:
        grupo_obj = grupo_resumen()
        grupo_obj.grupo = grupo.cGrupo
        grupo_obj.id = grupo.id
        indicadores = grupo.indicador_set.filter(lVigente=True).order_by('nOrden')
        for indicador in indicadores:
            # Listar todos los medios de verificación
            medios = indicador.medioverificacion_set.filter(lVigente=True).order_by('nOrden')
            # if not usuario.lRevisor:
            #     # Si no es revisor se filtra por oficina responsable
            #     medios = medios.filter(lVigente=True, oficinaResponsable=oficina).order_by('nOrden')
            items_medios = medios.count()
            for medio in medios:
                # Se lista las evidencias del periodo seleccionado
                evidencias = medio.evidencia_set.filter(periodo=periodo)
                grupo_obj.aprobados += evidencias.filter(idEstado='Aprobado').count()
                grupo_obj.observados += evidencias.filter(idEstado='Observado').count()
      
            resumen_obj.items += items_medios
            grupo_obj.items += items_medios#grupo_obj.pendientes + grupo_obj.aprobados + grupo_obj.observados
        grupo_obj.pendientes += grupo_obj.items - grupo_obj.aprobados - grupo_obj.observados
    
        if grupo_obj.items>0:
            resumen_obj.grupos.append(grupo_obj)
    return resumen_obj

def resumen_indicadores(grupos, periodo, oficina, usuario):
    resumen_obj = resumen()
    resumen_obj.grupos = []
    
    indicadores = grupos.indicador_set.filter(lVigente=True).order_by('nOrden')
    for indicador in indicadores:
        grupo_obj = grupo_resumen()
        grupo_obj.grupo = indicador.cIndicador
        grupo_obj.id = indicador.id
        # Listar todos los medios de verificación
        medios = indicador.medioverificacion_set.filter(lVigente=True).order_by('nOrden')
        # if not usuario.lRevisor:
        #     # Si no es revisor se filtra por oficina responsable
        #     medios = medios.filter(lVigente=True, oficinaResponsable=oficina).order_by('nOrden')
        items_medios = medios.count()
        for medio in medios:
            # Se lista las evidencias del periodo seleccionado
            evidencias = medio.evidencia_set.filter(periodo=periodo)
            grupo_obj.cargados += evidencias.filter(idEstado='Pendiente').count()
            grupo_obj.aprobados += evidencias.filter(idEstado='Aprobado').count()
            grupo_obj.observados += evidencias.filter(idEstado='Observado').count()
    
        resumen_obj.items += items_medios
        grupo_obj.pendientes += items_medios - grupo_obj.aprobados - grupo_obj.observados
        grupo_obj.items = grupo_obj.pendientes + grupo_obj.aprobados + grupo_obj.observados

        if grupo_obj.items > 0:
            resumen_obj.grupos.append(grupo_obj)
    return resumen_obj

def resumen_medios(medios, periodo, oficina, usuario):
    resumen_obj = resumen()
    resumen_obj.grupos = []

    # Listar todos los medios de verificación
    medios = medios.filter(lVigente=True).order_by('nOrden')
    # if not usuario.lRevisor:
    #     # Si no es revisor se filtra por oficina responsable
    #     medios = medios.filter(lVigente=True, oficinaResponsable=oficina).order_by('nOrden')
    resumen_obj.items = medios.count()
    
    for medio in medios:
        grupo_obj = grupo_resumen()
        grupo_obj.id = medio.id
        grupo_obj.grupo = medio.cTitulo
        grupo_obj.grupo2 = medio.cMedioVerificacion
        grupo_obj.lEdita = 0
        if medio.oficinaResponsable == oficina:
            grupo_obj.lEdita = 1
        
        # Se lista las evidencias del periodo seleccionado
        nDetalles=0
        if medio.evidencia_set.filter(periodo=periodo).count()>0:
            evidencias = medio.evidencia_set.filter(periodo=periodo)
            grupo_obj.archivos = evidencias.first().archivo_set.all().count()
            grupo_obj.revisiones = evidencias.first().revision_set.all().count()
            
            if evidencias.first().cDetalle1 != '':
                nDetalles=nDetalles+1
            if evidencias.first().cDetalle2 != '':
                nDetalles=nDetalles+1
            grupo_obj.detalles=nDetalles
        else:
            grupo_obj.archivos = 0
            grupo_obj.detalles=0

        resumen_obj.grupos.append(grupo_obj)
    
    return resumen_obj

def nombre_grupo_func(grupo, tipo):
    id=0
    if tipo==1:
        id = grupo.categoria_id
    elif tipo==2:
        id = grupo.grupo.categoria_id

    if id==1:
        return 'Condiciones'
    elif id==2:
        return 'Requerimientos'
    elif id==3:
        return 'Recomendaciones'
    elif id==4:
        return 'Estandares'
    elif id==5:
        return 'Renovaciones'
    else:
        return 'Otro Grupo'