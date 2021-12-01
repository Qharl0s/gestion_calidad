from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from evidencia.models import MedioVerificacion
from usuario.models import Usuario

@login_required
def condiciones(request):
  user = Usuario.objects.get(username=request.user.username)  
  grupos = obtener_grupos(user, 1)
  context = {'condiciones' : grupos, 'usuario':user, 'menu_condicion':"pcoded-trigger active"}
  return render(request, 'inicio/condiciones.html', context)

@login_required
def requerimientos(request):
  user = Usuario.objects.get(username=request.user.username)  
  grupos = obtener_grupos(user, 2)
  context = {'condiciones' : grupos, 'usuario':user, 'menu_requerimiento':"pcoded-trigger active"}
  return render(request, 'inicio/condiciones.html', context)

@login_required
def recomendaciones(request):
  user = Usuario.objects.get(username=request.user.username)  
  grupos = obtener_grupos(user, 3)
  context = {'condiciones' : grupos, 'usuario':user, 'menu_recomendacion':"pcoded-trigger active"}
  return render(request, 'inicio/condiciones.html', context)

@login_required
def guardar_evidencia(request):
  if request.method=="POST":
    try:
      pdf = request.FILES['fileEvidencia']
      idEvidencia = request.POST['idEvidencia']
      medio = MedioVerificacion.objects.get(id=idEvidencia)
      
      
      if medio.archivoPdf.name != '':
        fs_ = FileSystemStorage("media/")
        if fs_.exists(medio.archivoPdf.name):
            fs_.delete(medio.archivoPdf.name)
      
      user = Usuario.objects.get(username=request.user.username)
      
      medio.archivoPdf = pdf
      medio.dFechaCarga = datetime.now()
      medio.lRevisado = False
      medio.usuarioCarga = user
      medio.save()
      
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError as e:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la revisión, intente de nuevo.'})

@login_required
def guardar_revision(request):
  if request.method=="POST":
    try:
      user = Usuario.objects.get(username=request.user.username)
      medio = MedioVerificacion.objects.get(id=request.POST['idEvidencia'])
      medio.idEstado = int(request.POST['idEstado'])
      medio.cComentarioRevisor = request.POST['cComentario']
      medio.dFechaRevision = datetime.now()
      medio.lRevisado = True
      medio.usuarioRevisor = user
      medio.save()
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa'})
    except ValueError:
        return JsonResponse({"state":"error","cMensaje":'Ocurrió un error al intentar guardar la revisión, intente de nuevo.'})
      
@login_required
def listar_revision(request):
  if request.method == "POST":
    medio = MedioVerificacion.objects.get(id=request.POST['idEvidencia'])
    cEstado = "Pendiente"
    if medio.idEstado == 2:
      cEstado = "Observado"
    if medio.idEstado == 3:
      cEstado = "Aprobado"
      
    return JsonResponse({"dFecha":medio.dFechaRevision.strftime("%m/%d/%Y, %H:%M:%S"),"cComentario":medio.cComentarioRevisor, "cEstado": cEstado})
 
def obtener_grupos(user, idGrupo):
  if user.lRevisor or user.is_staff :
    evidencias = MedioVerificacion.objects.filter(lVigente=True)
  else:
    evidencias = user.oficina.evidencias.filter(lVigente=True)
  #Listar Indicadores vs Evidencia
  indicadores = []
  for evidencia in evidencias:
    cIndicadorDesc = evidencia.indicador.cIndicador+'<p><i>'+evidencia.indicador.cDescripcion+'</i></p>'
    if cIndicadorDesc not in indicadores:
      indicadores.append(cIndicadorDesc)
  
  evi_indi = {}
  for indicador in indicadores:
    evidencias_ = []
    for evidencia in evidencias:
      cIndicadorDesc = evidencia.indicador.cIndicador+'<p><i>'+evidencia.indicador.cDescripcion+'</i></p>'
      if cIndicadorDesc == indicador:
        evidencias_.append(evidencia)
    evi_indi[indicador] = evidencias_
  
  # listar grupos
  grupos = []
  for evidencia in evidencias:
    if evidencia.indicador.grupo.categoria.id == idGrupo and evidencia.indicador.grupo.cGrupo not in grupos:
      grupos.append(evidencia.indicador.grupo.cGrupo)
  # Listar indicadores por grupo
  ind_cond = {}
  for grupo in grupos:
    indicador_ = []
    for evidencia in evidencias:
      if evidencia.indicador.grupo.cGrupo == grupo:
        cIndicadorDesc = evidencia.indicador.cIndicador+'<p><i>'+evidencia.indicador.cDescripcion+'</i></p>'
        if cIndicadorDesc not in indicador_:
          indicador_.append(cIndicadorDesc)
    ind_cond[grupo] = indicador_
  
  indicador_grupo = {}
  for key, item in ind_cond.items():
    array = {}
    for it in item:
      array[it] = evi_indi[it]
    indicador_grupo[key] = array
    
  return indicador_grupo