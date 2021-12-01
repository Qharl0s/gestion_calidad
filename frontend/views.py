from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuario.models import Usuario

@login_required
def inicio(request):
  user = Usuario.objects.get(username=request.user.username)
  context = {'usuario':user, 'menu_inicio':"active"}
  return render(request, 'inicio/inicio.html', context)

