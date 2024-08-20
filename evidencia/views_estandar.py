from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from evidencia.models import Categoria, Evidencia, Evidencia_Todo, MedioVerificacion, Periodo, Grupo, Indicador, Archivo, Revision
from usuario.models import Oficina, Usuario
from evidencia.funciones import nombre_grupo_func, listar_objetos
from evidencia.validaciones import *


@login_required
def estandares(request, oficina_id=0, periodo_id=0):
  #Validaciones
  error_msg = valida_pre_estandar(oficina_id, periodo_id)

  usuario = request.user
  #Oficinas
  oficinas = Oficina.objects.filter(id=0).order_by('-cOficina')
  if usuario.lRevisor:
    oficinas = Oficina.objects.filter(lVigente=True, lAcreditacion=True)
  #Periodo
  periodos = Periodo.objects.filter(lVigente=True, categoria__id=4).order_by('-id')
  
  if periodo_id==0:
    periodo_seleccionado = periodos.first()
  else:
    periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  
  oficina_seleccionado = usuario.oficina
  if usuario.lRevisor and oficina_id>0:
    oficina_seleccionado = Oficina.objects.get(id=oficina_id)
  
  objetos = listar_objetos(categoria_id=4, grupo_id=0, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=oficina_seleccionado.id, es_estandar=1, es_revisor=usuario.lRevisor)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos, 
             'periodos':periodos, 'periodo_seleccionado':periodo_seleccionado,
             'oficinas':oficinas, 'oficina_seleccionado':oficina_seleccionado,
             'detalle_url':'indicadores', 'submenu':[], 'usuario': usuario, 
             'mostrar_oficinas': 1, 'mostrar_periodos':1, 'estandar':1,
             'url':'estandares'
            }
  return render(request, 'resumen.html', context)

@login_required
def indicadores_estandar(request, oficina_id, periodo_id, grupo_id):
  usuario = request.user
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  # #Oficina
  # oficinas = Oficina.objects.filter(lVigente=1, lAcreditacion=1).order_by('-cOficina')
  oficina_seleccionado = usuario.oficina
  if usuario.lRevisor:
    oficina_seleccionado = Oficina.objects.get(id=oficina_id)

  objetos = listar_objetos(categoria_id=0, grupo_id=grupo_id, indicador_id=0, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=oficina_seleccionado.id, es_estandar=1, es_revisor=usuario.lRevisor)

  context = {'URL_BASE':settings.URL_BASE,'objetos':objetos,'periodo_seleccionado':periodo_seleccionado,
             'oficina_seleccionado':oficina_seleccionado,
             'detalle_url':'medios', 
             'submenu':[{'nombre':'Estandares', 'url': settings.URL_BASE+'estandares/'+str(oficina_seleccionado.id)+'/'+str(periodo_seleccionado.id)}, ]
             , 'usuario': usuario, 'mostrar_periodos':1, 'mostrar_oficinas': 1, 'estandar':1,
             'url':'indicadores'
            }
  return render(request, 'resumen.html', context)

def medios_verificacion_estandar(request, oficina_id, periodo_id, indicador_id):
  usuario = Usuario.objects.get(username=request.user.username)
  #indicador
  indicador = Indicador.objects.get(id=indicador_id)
  #Periodo
  periodo_seleccionado = Periodo.objects.get(id=periodo_id)
  # #Oficina
  # oficinas = Oficina.objects.filter(lVigente=1, lAcreditacion=1).order_by('-cOficina')
  oficina_seleccionado = usuario.oficina
  if usuario.lRevisor:
    oficina_seleccionado = Oficina.objects.get(id=oficina_id)

  objetos = listar_objetos(categoria_id=0, grupo_id=0, indicador_id=indicador_id, medio_id=0, periodo_id=periodo_seleccionado.id,
                           oficina_id=oficina_id, es_estandar=1, es_revisor=usuario.lRevisor)
  
  # resumen = resumen_medios(medios, periodo_seleccionado, usuario.oficina, usuario)
  nombre_grupo = nombre_grupo_func(indicador, 2)

  context = {'URL_BASE':settings.URL_BASE,'usuario':usuario, 'medios':objetos,'periodo_seleccionado':periodo_seleccionado,
             'mostrar_periodos':1, 'mostrar_oficinas': 1, 'url':'medios', 'estandar':1,
             'oficina_seleccionado':oficina_seleccionado, 'indicador': indicador,
             'detalle_url':'', 
             'submenu':[
                {'nombre':'estandares', 'url': settings.URL_BASE+'estandares/'+str(oficina_seleccionado.id)+'/'+str(periodo_seleccionado.id)},
                {'nombre':'Indicadores', 'url': settings.URL_BASE+'indicadores/'+str(oficina_seleccionado.id)+'/'+str(periodo_seleccionado.id)+'/'+str(indicador.grupo.id)} 
              ] 
            }

  return render(request, 'medios_verificacion.html', context)