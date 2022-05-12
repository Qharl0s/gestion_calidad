from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from evidencia.models import MedioVerificacion
from usuario.models import Usuario

@login_required
def inicio(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_inicio':"active"}
  return render(request, 'inicio.html', context)

# def listar_grupos(user):
#   if user.lRevisor or user.is_staff :
#     evidencias = MedioVerificacion.objects.filter(lVigente=True)
#   else:
#     evidencias = user.oficina.evidencias.filter(lVigente=True)
    
  # listar grupos
  categorias = []
  for evidencia in evidencias:
    if evidencia.indicador.grupo.categoria.cCategoria not in categorias:
      categorias.append(evidencia.indicador.grupo.categoria.cCategoria)
  return categorias