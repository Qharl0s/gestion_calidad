from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from evidencia.models import Categoria, Evidencia, Evidencia_Todo, MedioVerificacion, Periodo, Grupo, Indicador, Archivo, Revision
from usuario.models import Oficina, Usuario
from evidencia.funciones import resumen_grupos, resumen_indicadores, resumen_medios, nombre_grupo_func

@login_required
def estandares(request, oficina_id=0):
  user = Usuario.objects.get(username=request.user.username)
  
  oficina = user.oficina
  oficinas = Oficina()
  if user.lRevisor:
    try:
      oficina = Oficina.objects.get(id=oficina_id)
    except Oficina.DoesNotExist:
      oficina = Oficina()
      oficina.id = 0
      oficina.cOficina = 'Seleccione Oficina..'
    oficinas = Oficina.objects.filter(lVigente=True, lAcreditacion=True)
  
  categoria = Categoria.objects.filter(id=4)
  
  context = {'categoria' : categoria, 'usuario':user, 'oficina': oficina, 'oficinas': oficinas, 'menu_estandar':"pcoded-trigger active", 'lAcreditacion':'true'}
  return render(request, 'resumen.html', context)

@login_required
def condiciones(request, periodo_id=0):
  usuario = request.user
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=1).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  categoria = Categoria.objects.filter(id=1)
  
  resumen = resumen_grupos(categoria, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario
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
  #Categorias
  categoria = Categoria.objects.filter(id=2)
  
  resumen = resumen_grupos(categoria, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario
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
  #Categorias
  categoria = Categoria.objects.filter(id=3)
  
  resumen = resumen_grupos(categoria, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario
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
  #Categorias
  categoria = Categoria.objects.filter(id=5)
  
  resumen = resumen_grupos(categoria, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario
             }
  return render(request, 'resumen.html', context)


@login_required
def indicadores(request, periodo_id, grupo_id):
  usuario = request.user
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  grupos = Grupo.objects.get(id=grupo_id)
  
  resumen = resumen_indicadores(grupos, periodo_seleccionado, usuario.oficina, usuario)
  nombre_grupo = nombre_grupo_func(grupos, 1)

  context = {'datos_resumen':resumen,'periodo_seleccionado':periodo_seleccionado
             , 'detalle_url':'medios', 
             'submenu':[{'nombre':nombre_grupo, 'url': 'http://'+request.get_host()+'/condiciones/'+str(periodo_seleccionado.id)}, ]
             , 'usuario': usuario
            }
  return render(request, 'resumen.html', context)

@login_required
def medios_verificacion(request, periodo_id, indicador_id):
  usuario = Usuario.objects.get(username=request.user.username)
  #indicador
  indicador = Indicador.objects.get(id=indicador_id)
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #medios
  medios = MedioVerificacion.objects.filter(indicador__id=indicador_id)
  # if not usuario.lRevisor:
  #   medios = medios.filter(indicador__id=indicador_id, oficinaResponsable=usuario.oficina)

  resumen = resumen_medios(medios, periodo_seleccionado, usuario.oficina, usuario)
  nombre_grupo = nombre_grupo_func(indicador, 2)

  context = {'usuario':usuario, 'medios':resumen,'periodo_seleccionado':periodo_seleccionado
            , 'detalle_url':'', 
             'submenu':[
                {'nombre':nombre_grupo, 'url': 'http://'+request.get_host()+'/condiciones/'+str(periodo_seleccionado.id)},
                {'nombre':'Indicadores', 'url': 'http://'+request.get_host()+'/indicadores/'+str(periodo_seleccionado.id)+'/'+str(indicador.grupo.id)} 
              ] 
            }

  return render(request, 'medios_verificacion.html', context)

# #################################################################################################################
# CRUD , Eventos y Complementarios
@login_required
def guardar_evidencia(request):
  if request.method=="POST":
    try:
      user = Usuario.objects.get(username=request.user.username)
      medio_verificacion = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      periodo = Periodo.objects.get(id=request.POST['idPeriodo'])

      if medio_verificacion.oficinaResponsable != request.user.oficina:
        return JsonResponse({"state":"error","cMensaje":'No perteneces a la oficina responsable'})
      
      evidencia = guarda_detalle_evi(medio_verificacion, periodo, request.POST['cDetalle1'], request.POST['cDetalle2'], user, guardar_existe=1)
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la evidencia, intente de nuevo.'})
    
@login_required
def guardar_archivo(request):
  if request.method=="POST":
    try:
      user = Usuario.objects.get(username=request.user.username)
      medio_verificacion = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      periodo = Periodo.objects.get(id=request.POST['idPeriodo'])

      if medio_verificacion.oficinaResponsable != request.user.oficina:
        return JsonResponse({"state":"error","cMensaje":'No perteneces a la oficina responsable'})
      
      evidencia = guarda_detalle_evi(medio_verificacion, periodo, '', '', user, guardar_existe=0)

      if 'fileEvidencia' in request.FILES:
        archivo = Archivo()
        archivo.evidencia = evidencia
        archivo.archivoPdf = request.FILES['fileEvidencia']
        archivo.usuario = user
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

def guarda_detalle_evi(medio_verificacion, periodo, detalle1, detalle2, user, guardar_existe):
  try:
    evidencia = Evidencia.objects.get(medioVerificacion=medio_verificacion, oficina=user.oficina, periodo=periodo)
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
    evidencia.save()

  return evidencia

@login_required
def obtener_evidencia(request):
  if request.method=="POST":
    user = Usuario.objects.get(username=request.user.username)
    try:
      evidencia = Evidencia.objects.get(medioVerificacion__id = request.POST['idMedioVerificacion'], periodo__id=request.POST['idPeriodo'])
      
      return JsonResponse({"state":"success", "cMensaje":"","cDetalle1":evidencia.cDetalle1, "cDetalle2":evidencia.cDetalle2})
    except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No se ha encontrado evidencia cargada.'})

@login_required
def listar_archivos(request):
  if request.method=="POST":
    try:
      try:
        evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedioVerificacion'], periodo__id=request.POST['idPeriodo'])
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
        evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedio'], periodo__id=request.POST['idPeriodo'])
      except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No se encontró evidencia cargada.'})

      evidencia.idEstado = request.POST['cEstado']
      evidencia.save()

      revision = Revision()
      revision.evidencia = evidencia
      revision.cRevision = request.POST['cComentario']
      revision.idEstado = request.POST['cEstado']
      revision.dFecha = datetime.now()
      revision.usuario = user
      revision.lVigente = True
      revision.save()
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la revisión, intente de nuevo.'})
      
@login_required
def listar_revision(request):
  if request.method == "POST":
    try:
      evidencia = Evidencia.objects.get(medioVerificacion__id=request.POST['idMedio'], periodo__id=request.POST['idPeriodo'])
      revisiones = Revision.objects.filter(evidencia=evidencia).values('id', 'cRevision', 'dFecha', 'idEstado', 'usuario__username').order_by('-dFecha')
      # evidencia.dFechaRevision.strftime("%m/%d/%Y, %H:%M:%S")
      return JsonResponse({"state":"success","revisiones": list(revisiones), 'lRevisor':request.user.lRevisor})
    except Evidencia.DoesNotExist:
      return JsonResponse({"state":"error", "revisiones": list()})

@login_required
def evidencias(request, periodo_id, medio_id):
  usuario = Usuario.objects.get(username=request.user.username)
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #medios
  medios = MedioVerificacion.objects.filter(id=medio_id, oficinaResponsable=usuario.oficina)

  resumen = resumen_medios(medios, periodo_seleccionado, usuario.oficina, usuario)

  context = {'medios':resumen,'periodo_seleccionado':periodo_seleccionado
            , 'detalle_url':'', 
             'submenu':[
                # {'nombre':'Condiciones', 'url': 'http://'+request.get_host()+'/condiciones/'+str(periodo_seleccionado.id)},
                # {'nombre':'Indicadores', 'url': 'http://'+request.get_host()+'/indicadores/'+str(periodo_seleccionado.id)+'/'+str(indicador.grupo.id)} 
              ] 
            }

  return render(request, 'evidencias.html', context)