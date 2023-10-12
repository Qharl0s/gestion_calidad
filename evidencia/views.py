from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from evidencia.models import Categoria, Evidencia, Evidencia_Todo, MedioVerificacion
from usuario.models import Oficina, Usuario

# @login_required
# def evidencia(request, id_medio_verificacion):
#   user = Usuario.objects.get(username=request.user.username)
#   oficina = user.oficina
#   try:
#     medio = MedioVerificacion.objects.get(id=id_medio_verificacion)
#   except MedioVerificacion.DoesNotExist:
#     medio = MedioVerificacion()
    
#   evidencia = Evidencia.objects.get(medioVerificacion=medio, oficina=oficina)
  
#   context = {'usuario':user, 'idMedioVerificacion':id_medio_verificacion, 'evidencia': evidencia}
  
#   return render(request, 'evidencia.html', context)

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
  return render(request, 'medios_verificacion.html', context)

@login_required
def condiciones(request):
  user = Usuario.objects.get(username=request.user.username)  
  
  oficina = user.oficina
  categoria = Categoria.objects.filter(id=1)
  
  context = {'categoria' : categoria, 'usuario':user, 'oficina':oficina, 'menu_condicion':"pcoded-trigger active",
  #'evidencias':evidencias
  }
  return render(request, 'medios_verificacion.html', context)

@login_required
def requerimientos(request):
  user = Usuario.objects.get(username=request.user.username)
  
  oficina = user.oficina
  categoria = Categoria.objects.filter(id=2)
  
  context = {'categoria' : categoria, 'usuario':user, 'oficina':oficina, 'menu_requerimiento':"pcoded-trigger active"}
  return render(request, 'medios_verificacion.html', context)

@login_required
def recomendaciones(request):
  user = Usuario.objects.get(username=request.user.username)  

  oficina = user.oficina
  categoria = Categoria.objects.filter(id=3)
  
  context = {'categoria' : categoria, 'usuario':user, 'oficina':oficina, 'menu_recomendacion':"pcoded-trigger active"}
  return render(request, 'medios_verificacion.html', context)

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
      
    return JsonResponse({"dFecha":evidencia.dFechaRevision.strftime("%m/%d/%Y, %H:%M:%S"),"cComentario":evidencia.cComentarioRevisor, "cEstado": cEstado})
 
# def obtener_grupos(user, idGrupo):
#   if user.lRevisor or user.is_staff :
#     evidencias = MedioVerificacion.objects.filter(lVigente=True)
#   else:
#     evidencias = user.oficina.evidencias.filter(lVigente=True)
#   #Listar Indicadores vs Evidencia
#   indicadores = []
#   for evidencia in evidencias:
#     cIndicadorDesc = evidencia.indicador.cIndicador+'<p><i>'+evidencia.indicador.cDescripcion+'</i></p>'
#     if cIndicadorDesc not in indicadores:
#       indicadores.append(cIndicadorDesc)
  
#   evi_indi = {}
#   for indicador in indicadores:
#     evidencias_ = []
#     for evidencia in evidencias:
#       cIndicadorDesc = evidencia.indicador.cIndicador+'<p><i>'+evidencia.indicador.cDescripcion+'</i></p>'
#       if cIndicadorDesc == indicador:
#         evidencias_.append(evidencia)
#     evi_indi[indicador] = evidencias_
  
#   # listar grupos
#   grupos = []
#   for evidencia in evidencias:
#     if evidencia.indicador.grupo.categoria.id == idGrupo and evidencia.indicador.grupo.cGrupo not in grupos:
#       grupos.append(evidencia.indicador.grupo.cGrupo)
#   # Listar indicadores por grupo
#   ind_cond = {}
#   for grupo in grupos:
#     indicador_ = []
#     for evidencia in evidencias:
#       if evidencia.indicador.grupo.cGrupo == grupo:
#         cIndicadorDesc = evidencia.indicador.cIndicador+'<p><i>'+evidencia.indicador.cDescripcion+'</i></p>'
#         if cIndicadorDesc not in indicador_:
#           indicador_.append(cIndicadorDesc)
#     ind_cond[grupo] = indicador_
  
#   indicador_grupo = {}
#   for key, item in ind_cond.items():
#     array = {}
#     for it in item:
#       array[it] = evi_indi[it]
#     indicador_grupo[key] = array
    
#   return indicador_grupo