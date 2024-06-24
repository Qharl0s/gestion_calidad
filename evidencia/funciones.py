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
            if not usuario.lRevisor:
                # Si no es revisor se filtra por oficina responsable
                medios = medios.filter(lVigente=True, oficinaResponsable=oficina).order_by('nOrden')
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
        if not usuario.lRevisor:
            # Si no es revisor se filtra por oficina responsable
            medios = medios.filter(lVigente=True, oficinaResponsable=oficina).order_by('nOrden')
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
    if not usuario.lRevisor:
        # Si no es revisor se filtra por oficina responsable
        medios = medios.filter(lVigente=True, oficinaResponsable=oficina).order_by('nOrden')
    
    for medio in medios:
        grupo_obj = grupo_resumen()
        grupo_obj.id = medio.id
        grupo_obj.grupo = medio.cTitulo
        grupo_obj.grupo2 = medio.cMedioVerificacion
        
        # Se lista las evidencias del periodo seleccionado
        if medio.evidencia_set.filter(periodo=periodo).count()>0:
            evidencias = medio.evidencia_set.filter(periodo=periodo)
            grupo_obj.archivos = evidencias.archivo_set.all.count()
        else:
            grupo_obj.archivos = 0

        resumen_obj.grupos.append(grupo_obj)
    
    return resumen_obj
