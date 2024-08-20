from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from evidencia.models import Categoria, Evidencia, Evidencia_Todo, MedioVerificacion, Periodo, Grupo, Indicador, Archivo, Revision
from usuario.models import Oficina, Usuario
from evidencia.funciones import nombre_grupo_func, listar_objetos

@login_required
def reportes1(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'URL_BASE':settings.URL_BASE,'usuario':user, 'menu_inicio':"active"}
  return render(request, 'reporte1.html', context)

@login_required
def reportes2(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'URL_BASE':settings.URL_BASE,'usuario':user, 'menu_inicio':"active"}
  return render(request, 'reporte2.html', context)

@login_required
def reportes3(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'URL_BASE':settings.URL_BASE,'usuario':user, 'menu_inicio':"active"}
  return render(request, 'reporte3.html', context)

@login_required
def condiciones(request, periodo_id=0):
  usuario = request.user
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=1).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  
  objetos = listar_objetos(categoria_id=1, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=usuario.oficina.id, es_estandar=0, es_revisor=usuario.lRevisor)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario, 'mostrar_periodos':1
             }
  return render(request, 'resumen.html', context)

@login_required
def requerimientos(request, periodo_id=0):
  usuario = request.user
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=2).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  
  objetos = listar_objetos(categoria_id=2, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=usuario.oficina.id, es_estandar=0, es_revisor=usuario.lRevisor)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario, 'mostrar_periodos':1
             }
  return render(request, 'resumen.html', context)

@login_required
def recomendaciones(request, periodo_id=0):
  usuario = request.user
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=3).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
 
  objetos = listar_objetos(categoria_id=3, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=usuario.oficina.id, es_estandar=0, es_revisor=usuario.lRevisor)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario, 'mostrar_periodos':1
             }
  return render(request, 'resumen.html', context)

@login_required
def renovaciones(request, periodo_id=0):
  usuario = request.user
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=1).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  
  objetos = listar_objetos(categoria_id=5, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=usuario.oficina.id, es_estandar=0, es_revisor=usuario.lRevisor)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario, 'mostrar_periodos':1
             }
  return render(request, 'resumen.html', context)


@login_required
def indicadores(request, periodo_id, grupo_id):
  usuario = request.user
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  grupos = Grupo.objects.get(id=grupo_id)

  objetos = listar_objetos(categoria_id=0, grupo_id=grupo_id, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=usuario.oficina.id, es_estandar=0, es_revisor=usuario.lRevisor)
  
  nombre_grupo = nombre_grupo_func(grupos, 1)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos,'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'medios', 
             'submenu':[{'nombre':nombre_grupo, 'url': settings.URL_BASE+nombre_grupo+'/'+str(periodo_seleccionado.id)}, ]
             , 'usuario': usuario, 'mostrar_periodos':1, 'mostrar_oficinas': 0
            }
  return render(request, 'resumen.html', context)

@login_required
def medios_verificacion(request, periodo_id, indicador_id):
  usuario = Usuario.objects.get(username=request.user.username)
  #indicador
  indicador = Indicador.objects.get(id=indicador_id)
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)

  objetos = listar_objetos(categoria_id=0, grupo_id=0, indicador_id=indicador_id, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=usuario.oficina.id, es_estandar=0, es_revisor=usuario.lRevisor)
  
  # resumen = resumen_medios(medios, periodo_seleccionado, usuario.oficina, usuario)
  nombre_grupo = nombre_grupo_func(indicador, 2)

  context = {'URL_BASE':settings.URL_BASE,'usuario':usuario, 'medios':objetos,'periodo_seleccionado':periodo_seleccionado, 
             'mostrar_periodos':1, 'mostrar_oficinas': 0, 'indicador':indicador,
             'detalle_url':'', 
             'submenu':[
                {'nombre':nombre_grupo, 'url': settings.URL_BASE+nombre_grupo+'/'+str(periodo_seleccionado.id)},
                {'nombre':'Indicadores', 'url': settings.URL_BASE+'indicadores/'+str(periodo_seleccionado.id)+'/'+str(indicador.grupo.id)} 
              ] 
            }

  return render(request, 'medios_verificacion.html', context)

# #################################################################################################################
# CRUD , Eventos y Complementarios
@login_required
def guardar_evidencia(request):
  if request.method=="POST":
    try:
      usuario = Usuario.objects.get(username=request.user.username)
      medio_verificacion = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      periodo = Periodo.objects.get(id=request.POST['idPeriodo'])

      if not usuario.oficina.lAcreditacion and medio_verificacion.oficinaResponsable != usuario.oficina:
        return JsonResponse({"state":"error","cMensaje":'No perteneces a la oficina responsable'})
      
      evidencia = guarda_detalle_evi(medio_verificacion, periodo, request.POST['cDetalle1'], request.POST['cDetalle2'], usuario, guardar_existe=1)
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la evidencia, intente de nuevo.'})
    
@login_required
def guardar_archivo(request):
  if request.method=="POST":
    try:
      usuario = Usuario.objects.get(username=request.user.username)
      medio_verificacion = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      periodo = Periodo.objects.get(id=request.POST['idPeriodo'])

      if not usuario.oficina.lAcreditacion and medio_verificacion.oficinaResponsable != usuario.oficina:
        return JsonResponse({"state":"error","cMensaje":'No perteneces a la oficina responsable'})
      
      evidencia = guarda_detalle_evi(medio_verificacion, periodo, '', '', usuario, guardar_existe=0)

      if 'fileEvidencia' in request.FILES:
        archivo = Archivo()
        archivo.evidencia = evidencia
        archivo.archivoPdf = request.FILES['fileEvidencia']
        archivo.usuario = usuario
        archivo.dFecha = datetime.now()
        archivo.lVigente = True
        archivo.save()
      else:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error, no se enconctró archivo a cargar, intente de nuevo.'})
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar el archivo, intente de nuevo.'})

@login_required
def eliminar_archivo(request):
  if request.method=="POST":
    try:
      archivo = Archivo.objects.get(id=request.POST['idArchivo'])

      if archivo.evidencia.medioVerificacion.oficinaResponsable != request.user.oficina:
        return JsonResponse({"state":"error","cMensaje":'No perteneces a la oficina responsable'})

      archivo.delete()
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar eliminar el archivo, intente de nuevo.'})

def guarda_detalle_evi(medio_verificacion, periodo, detalle1, detalle2, user, guardar_existe, escala_id=0):
  try:
    evidencia = Evidencia.objects.get(medioVerificacion=medio_verificacion, oficina=user.oficina, periodo=periodo, lFinalizado=False)
    existe=1
  except Evidencia.DoesNotExist:
    evidencia = Evidencia()
    evidencia.idEstado = 'Cargado'
    existe=0
  
  # Guarda si viene de detalle, pero, si viene de archivo inserta solo si no existe
  if guardar_existe==0 and existe==0:
    guardar_existe=1
  
  if guardar_existe==1:
    evidencia.oficina = user.oficina
    evidencia.medioVerificacion = medio_verificacion
    evidencia.periodo = periodo
    evidencia.lRevisado = False
    evidencia.usuarioCarga = user
    evidencia.dFechaCarga = datetime.now()
    evidencia.cDetalle1 = detalle1
    evidencia.cDetalle2 = detalle2
    if escala_id>0:
      evidencia.idEscala = escala_id
    evidencia.save()

  return evidencia

@login_required
def obtener_evidencia(request):
  if request.method=="POST":
    user = Usuario.objects.get(username=request.user.username)
    oficina_id = int(request.POST['idOficina'])
    medio = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
    if not request.user.lRevisor and medio.oficinaResponsable is None:
      oficina_id = request.user.oficina.id
    try:
      evidencia = Evidencia.objects.get(medioVerificacion__id = request.POST['idMedioVerificacion'], periodo__id=request.POST['idPeriodo'], lFinalizado=False)
      if oficina_id>0:
        evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedioVerificacion'], periodo__id=request.POST['idPeriodo'], oficina__id=oficina_id, lFinalizado=False)
      
      return JsonResponse({"state":"success", "cMensaje":"","cDetalle1":evidencia.cDetalle1, "cDetalle2":evidencia.cDetalle2})
    except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No se ha encontrado evidencia cargada.'})

@login_required
def listar_archivos(request):
  if request.method=="POST":
    try:
      oficina_id = int(request.POST['idOficina'])
      medio = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      if not request.user.lRevisor and medio.oficinaResponsable is None:
        oficina_id = request.user.oficina.id
      
      try:
        evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedioVerificacion'], periodo__id=request.POST['idPeriodo'], lFinalizado=False)
        if oficina_id>0:
          evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedioVerificacion'], periodo__id=request.POST['idPeriodo'], oficina__id=oficina_id, lFinalizado=False)
      except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No hay evidenicia cargada', 'archivos':list()})
      try:
        archivos = evidencia.archivo_set.all().values('archivoPdf', 'dFecha', 'usuario__username', 'id').order_by('-id')
      except Archivo.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No hay archivos cargados', 'archivos':list()})
      return JsonResponse({"state":"success", "archivos":list(archivos)})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar listar los archivos, intente de nuevo.'})

    
@login_required
def guardar_revision(request):
  if request.method=="POST":
    try:
      user = Usuario.objects.get(username=request.user.username)
      if not user.lRevisor:
        return JsonResponse({"state":"error","cMensaje":'No tiene perfil de revisor.'})
      
      try:
        medio = MedioVerificacion.objects.get(id=request.POST['idMedio'])
      except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No se encontró el Medio de Verificación.'})

      try:
        evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedio'], periodo__id=request.POST['idPeriodo'], lFinalizado=False)
      except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No se encontró evidencia cargada.'})
      
      evidencia.idEstado = request.POST['cEstado']
      #Si es Estandar al aprobarse se actualiza a Finalizado
      if medio.indicador.grupo.categoria.id == 4 and request.POST['cEstado']=='Aprobado':
        evidencia.lFinalizado = True
      evidencia.save()

      revision = Revision()
      revision.evidencia = evidencia
      revision.cRevision = request.POST['cComentario']
      revision.idEstado = request.POST['cEstado']
      revision.dFecha = datetime.now()
      revision.usuario = user
      revision.lVigente = True
      revision.save()

      #Al ser aprobado se registra nueva evidencia en vacio
      if medio.indicador.grupo.categoria.id == 4 and request.POST['cEstado']=='Aprobado':
        escala_id = int(evidencia.idEscala) + 1
        if escala_id < 10:
          evidencia2 = guarda_detalle_evi(medio, evidencia.periodo, '', '', evidencia.usuarioCarga, guardar_existe=0, escala_id=escala_id)
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la revisión, intente de nuevo.'})
      
@login_required
def listar_revision(request):
  if request.method == "POST":
    try:
      evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedio'], periodo__id=request.POST['idPeriodo'], lFinalizado=False)
      revisiones = Revision.objects.filter(evidencia=evidencia).values('id', 'cRevision', 'dFecha', 'idEstado', 'usuario__username').order_by('-dFecha')
      # evidencia.dFechaRevision.strftime("%m/%d/%Y, %H:%M:%S")
      return JsonResponse({"state":"success","revisiones": list(revisiones), 'lRevisor':request.user.lRevisor})
    except Evidencia.DoesNotExist:
      return JsonResponse({"state":"error", "revisiones": list()})
