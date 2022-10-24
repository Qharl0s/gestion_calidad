from django.http.response import HttpResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from evidencia.models import MedioVerificacion
from usuario.models import Usuario
from django.http import JsonResponse

@login_required
def inicio(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_inicio':"active"}
  return render(request, 'inicio.html', context)

@login_required
def perfil(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user}
  return render(request, 'perfil.html', context)

@login_required
def guardar_datos(request):
  user = Usuario.objects.get(username=request.user.username)
  user.email = request.POST['email']
  user.cNombres = request.POST['nombres']
  user.save()
  return JsonResponse({"state":"success","cMensaje":'Operación exitosa.'})

@login_required
def actualizar_password(request):
  user = Usuario.objects.get(username=request.user.username)
  
  if user.check_password(request.POST['password_actual']):
    if request.POST['nuevo_password1'] == request.POST['nuevo_password2']:
      user.set_password(request.POST['nuevo_password1'])
      user.save()
      return JsonResponse({"state":"success","cMensaje":'Operación exitosa.'})
    else:
      return JsonResponse({"state":"error","cMensaje":'Los password nuevos no coinciden.'})
  else:
    return JsonResponse({"state":"error","cMensaje":'El password actual no coincide.'})

# def listar_grupos(user):
#   if user.lRevisor or user.is_staff :
#     evidencias = MedioVerificacion.objects.filter(lVigente=True)
#   else:
#     evidencias = user.oficina.evidencias.filter(lVigente=True)
    
  # listar grupos
  # categorias = []
  # for evidencia in evidencias:
  #   if evidencia.indicador.grupo.categoria.cCategoria not in categorias:
  #     categorias.append(evidencia.indicador.grupo.categoria.cCategoria)
  # return categorias