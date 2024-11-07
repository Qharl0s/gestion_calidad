from django.http.response import HttpResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from evidencia.models import MedioVerificacion, Periodo
from usuario.models import Usuario
from evidencia.funciones import *
from django.http import JsonResponse
from evidencia.graficos import get_grafico_barra, get_grafico_pie

@login_required
def inicio(request):
  usuario = Usuario.objects.get(username=request.user.username)
  periodos = Periodo.objects.filter(lFinalizado=False, lVigente=True)
  es_estandar = 0
  if usuario.oficina.lAcreditacion:
    es_estandar = 1
  objetos = lista_categorias(periodos, oficina_id=usuario.oficina.id, es_estandar=es_estandar, es_revisor=usuario.lRevisor)

  aprobados = 0
  observados = 0
  pendientes = 0
  for obj in objetos:
    aprobados += obj.datos_objeto.aprobados
    observados += obj.datos_objeto.observados
    pendientes += obj.datos_objeto.pendientes
  
  chart_barra_asignados_inicio = get_grafico_barra('Estado de Evidencias', objetos, 'grafico_barra_asignados')
  chart_pie_asignados_inicio = get_grafico_pie('Medios de Verificación Asignados', objetos, 'grafico_piechart_asignados')

  context = {'URL_BASE':settings.URL_BASE,'usuario':usuario, 'menu_inicio':"active", 'objetos': objetos,
             'es_estandar':es_estandar, 
             'chart_barra_asignados_inicio':chart_barra_asignados_inicio, 
             'chart_pie_asignados_inicio':chart_pie_asignados_inicio
             , 'aprobados': aprobados, 'observados': observados, 'pendientes':pendientes}
  return render(request, 'inicio.html', context)

@login_required
def perfil(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'URL_BASE':settings.URL_BASE,'usuario':user}
  return render(request, 'perfil.html', context)

@login_required
def guardar_datos(request):
  user = Usuario.objects.get(username=request.user.username)
  user.email = request.POST['email']
  user.cNombres = request.POST['nombres']
  user.save()
  return JsonResponse({"state":"success","cMensaje":'Operación exitosa.'})

@login_required
def guardar_foto(request):
  user = Usuario.objects.get(username=request.user.username)
  user.foto = request.FILES['foto']
  user.save()
  return JsonResponse({"state":"success","cMensaje":'Operación exitosa.'})

@login_required
def actualizar_password(request):
  user = Usuario.objects.get(username=request.user.username)
  
  # if user.check_password(request.POST['password_actual']):
  if request.POST['nuevo_password1'] == request.POST['nuevo_password2']:
    user.set_password(request.POST['nuevo_password1'])
    user.save()
    return JsonResponse({"state":"success","cMensaje":'Operación exitosa.'})
  else:
    return JsonResponse({"state":"error","cMensaje":'Los password nuevos no coinciden.'})
 
@login_required
def reporte_avance(request, categoria_id=0, periodo_id=0):
  usuario = request.user
  periodos = Periodo.objects.filter(lVigente=1, categoria_id=categoria_id).order_by('-id')
  periodo_seleccionado = periodos.first()
  if periodo_id>0:
    try:
      periodo_seleccionado = periodos.get(id=periodo_id)
    except Periodo.DoesNotExist:
      periodo_seleccionado = periodos.first()

  es_estandar = 1 if categoria_id==4 else 0
  es_revisor = 1 if usuario.lRevisor else 0

  objetos = listar_objetos(categoria_id,0,0,0,periodo_seleccionado.id,usuario.oficina.id,es_estandar,es_revisor)
  grafico = get_grafico_barra('Avance de '+nombre_grupo_func(None, 0, categoria_id), objetos, 'avance_rpt_barras')

  context = {'URL_BASE':settings.URL_BASE,'usuario':usuario, 'menu_reportes':"active pcoded-trigger",
             "mostrar_periodos":1,"periodos":periodos, 'periodo_seleccionado': periodo_seleccionado, 
             'es_estandar': es_estandar,'grafico_barras':grafico
             }
  return render(request, 'reporte_avances.html', context)

@login_required
def reporte_detalle(request, categoria_id=0, periodo_id=0):
  user = Usuario.objects.get(username=request.user.username)
  periodos = Periodo.objects.filter(categoria_id=categoria_id).order_by('-cPeriodo')
  categoria = []
  if categoria_id>0:
    categoria = Categoria.objects.get(id=categoria_id)
  periodo_seleccionado = []
  if periodo_id>0:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  evidencias = Evidencia.objects.filter(medioVerificacion__indicador__grupo__categoria_id=categoria_id, periodo_id=periodo_id).order_by('medioVerificacion__id')
  context = {'URL_BASE':settings.URL_BASE,'usuario':user, 'menu_reportes':"active", 
             "evidencias":evidencias, 'periodos':periodos, 'periodo_seleccionado': periodo_seleccionado, 'categoria':categoria,
             'mostrar_periodos': 1}
  return render(request, 'reporte_detalle.html', context)
