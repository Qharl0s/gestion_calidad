from django.db import models
from django.contrib.auth.models import AbstractUser

class Oficina(models.Model):
  cOficina = models.CharField('Oficina', max_length=120, default='')
  lAcreditacion = models.BooleanField('Acreditación',default=False)
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cOficina

class Usuario(AbstractUser):
    oficina = models.ForeignKey(Oficina, on_delete=models.PROTECT, blank=True, null=True)
    cNombres = models.CharField('Nombres y Apellidos', max_length=120, null=True)
    cCargo = models.CharField('Cargo', max_length=120, null=True)
    lRevisor = models.BooleanField('Revisor', null=True, default=False)
    lVigente = models.BooleanField('Vigente', default=True)
    foto = models.ImageField(upload_to='foto/', blank=True, null=True, default='')