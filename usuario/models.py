from django.db import models
from django.contrib.auth.models import AbstractUser

class Oficina(models.Model):
  cOficina = models.CharField('Oficina', max_length=120, default='')
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cOficina

class Usuario(AbstractUser):
    oficina = models.ForeignKey(Oficina, on_delete=models.PROTECT, blank=True, null=True)
    cNombres = models.CharField('Nombres y Apellidos', max_length=120, null=True)
    cCargo = models.CharField('Cargo', max_length=120, null=True)
    lRevisor = models.BooleanField('Revisor', null=True)
    lVigente = models.BooleanField('Vigente', default=True)