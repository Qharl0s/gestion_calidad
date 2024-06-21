from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from evidencia.models import Categoria, Evidencia, Evidencia_Todo, MedioVerificacion, Periodo, Grupo
from usuario.models import Oficina, Usuario
from evidencia.funciones import resumen_grupos, resumen_indicadores

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
  usuario = Usuario.objects.get(username=request.user.username)
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=1).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  categoria = Categoria.objects.filter(id=1)
  
  resumen = resumen_grupos(categoria, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado}
  return render(request, 'resumen.html', context)

@login_required
def requerimientos(request, periodo_id=0):
  usuario = Usuario.objects.get(username=request.user.username)
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=2).order_by('-id')
  if periodo_id==0:
    periodo_seleccionado = periodos[0]  
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  categoria = Categoria.objects.filter(id=2)
  
  resumen = resumen_grupos(categoria, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen, 'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado}
  return render(request, 'resumen.html', context)

@login_required
def recomendaciones(request):
  user = Usuario.objects.get(username=request.user.username)  

  oficina = user.oficina
  categoria = Categoria.objects.filter(id=3)
  
  context = {'categoria' : categoria, 'usuario':user, 'oficina':oficina, 'menu_recomendacion':"pcoded-trigger active"}
  return render(request, 'resumen.html', context)

@login_required
def guardar_evidencia(request):
  if request.method=="POST":
    try:
      if 'fileEvidencia' in request.FILES:
        pdf = request.FILES['fileEvidencia']
      
      user = Usuario.objects.get(username=request.user.username)
      medio_verificacion = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      
      try:
        evidencia = Evidencia.objects.get(oficina=user.oficina, medioVerificacion = medio_verificacion)
        if evidencia.archivoPdf.name != '' and 'fileEvidencia' in request.FILES:
          fs_ = FileSystemStorage("media/")
          if fs_.exists(evidencia.archivoPdf.name):
              fs_.delete(evidencia.archivoPdf.name)
      
      except Evidencia.DoesNotExist:
        evidencia = Evidencia()

      if 'fileEvidencia' in request.FILES:
        evidencia.archivoPdf = pdf
      
      evidencia.oficina = user.oficina
      evidencia.medioVerificacion = medio_verificacion
      evidencia.dFechaCarga = datetime.now()
      evidencia.lRevisado = False
      evidencia.usuarioCarga = user
      evidencia.cDetalle1 = request.POST['cDetalle1']
      evidencia.cDetalle2 = request.POST['cDetalle2']
      evidencia.idEstado = 'Cargado'
      evidencia.save()
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la evidencia, intente de nuevo.'})

@login_required
def obtener_evidencia(request):
  if request.method=="POST":
    try:
      medio_verificacion = MedioVerificacion.objects.get(id=request.POST['idMedioVerificacion'])
      user = Usuario.objects.get(username=request.user.username)
      oficina = Oficina.objects.get(id=request.POST['idOficina'])
      evidencia = Evidencia.objects.get(oficina=oficina, medioVerificacion = medio_verificacion)
      
      return JsonResponse({"state":"success", "cMensaje":"","cDetalle1":evidencia.cDetalle1, "cDetalle2":evidencia.cDetalle2, "cArchivoName": evidencia.archivoPdf.name})
    except Evidencia.DoesNotExist:
        return JsonResponse({"state":"error","cMensaje":'No se ha encontrado evidencia cargada.'})
    
    
@login_required
def guardar_revision(request):
  if request.method=="POST":
    try:
      user = Usuario.objects.get(username=request.user.username)
      evidencia = Evidencia.objects.get(id=request.POST['idEvidencia'])
      evidencia.idEstado = request.POST['idEstado']
      evidencia.cComentarioRevisor = request.POST['cComentario']
      evidencia.dFechaRevision = datetime.now()
      evidencia.lRevisado = True
      evidencia.usuarioRevisor = user
      evidencia.save()
      
      if evidencia.idEstado == 'Aprobado':
        try:
          evidencia_todo = Evidencia_Todo.objects.get(oficina=evidencia.oficina, medioVerificacion = evidencia.medioVerificacion, idEscala=evidencia.idEscala)
        except Evidencia_Todo.DoesNotExist:
          evidencia_todo = Evidencia_Todo()
        
        evidencia_todo.medioVerificacion = evidencia.medioVerificacion
        evidencia_todo.oficina = evidencia.oficina
        evidencia_todo.idEstado = 'Aprobado'
        evidencia_todo.idEscala = evidencia.idEscala
        evidencia_todo.usuarioCarga = evidencia.usuarioCarga
        evidencia_todo.cDetalle1 = evidencia.cDetalle1
        evidencia_todo.cDetalle2 = evidencia.cDetalle2
        evidencia_todo.archivoPdf = evidencia.archivoPdf
        evidencia_todo.dFechaCarga = evidencia.dFechaCarga
        evidencia_todo.lRevisado = evidencia.lRevisado
        evidencia_todo.usuarioRevisor = evidencia.usuarioRevisor
        evidencia_todo.cComentarioRevisor = evidencia.cComentarioRevisor
        evidencia_todo.dFechaRevision = evidencia.dFechaRevision
        evidencia_todo.save()
        # Se reinicia datos de la evidencia
        if evidencia.oficina.lAcreditacion :
          if evidencia.archivoPdf.name != '':
            fs_ = FileSystemStorage("media/")
            if fs_.exists(evidencia.archivoPdf.name):
                fs_.delete(evidencia.archivoPdf.name)
          evidencia.archivoPdf = None
          evidencia.dFechaCarga = None
          evidencia.idEstado = 'Pendiente'
          evidencia.cDetalle1 = ''
          evidencia.cDetalle2 = ''
          evidencia.lRevisado = False
          evidencia.usuarioRevisor = None
          evidencia.cComentarioRevisor = None
          evidencia.dFechaRevision = None
          # Agregar Escala o Finalizar
          if evidencia.oficina.lAcreditacion :
            evidencia.idEscala = str(int(evidencia.idEscala)+1)
          else:
            evidencia.idEscala = '10'
          evidencia.save()
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la revisión, intente de nuevo.'})
      
@login_required
def listar_revision(request):
  if request.method == "POST":
    evidencia = Evidencia.objects.get(id=request.POST['idEvidencia'])
    cEstado = "Pendiente"
    if evidencia.idEstado == 2:
      cEstado = "Observado"
    if evidencia.idEstado == 3:
      cEstado = "Aprobado"
    
    fecha = ''
    if evidencia.dFechaRevision is not None:
      evidencia.dFechaRevision.strftime("%m/%d/%Y, %H:%M:%S")

    return JsonResponse({"dFecha": fecha,"cComentario":evidencia.cComentarioRevisor, "cEstado": evidencia.idEstado})
 
@login_required
def indicadores(request, periodo_id, grupo_id):
  usuario = Usuario.objects.get(username=request.user.username)
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  grupos = Grupo.objects.get(id=grupo_id)
  
  resumen = resumen_indicadores(grupos, periodo_seleccionado, usuario.oficina, usuario)

  context = {'datos_resumen':resumen,'periodo_seleccionado':periodo_seleccionado}
  return render(request, 'resumen.html', context)

@login_required
def indicadores(request, periodo_id, indicador_id):
  usuario = Usuario.objects.get(username=request.user.username)
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  #Categorias
  medios = MedioVerificacion.objects.filter(indicador__id=indicador_id)

  context = {'medios':medios,'periodo_seleccionado':periodo_seleccionado}

  return render(request, 'medios_verificacion.html', context)