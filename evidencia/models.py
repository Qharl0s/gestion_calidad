from django.db import models
from usuario.models import Usuario, Oficina

class Categoria(models.Model):
  cCategoria = models.CharField('Categoria', max_length=360, default='')
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cCategoria

class Grupo(models.Model):
  categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
  cGrupo = models.CharField('Grupo', max_length=360, default='')
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cGrupo

class Indicador(models.Model):
  grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
  cIndicador = models.CharField('Indicador', max_length=360, default='')
  cDescripcion = models.CharField('Descripción', max_length=360, default='')
  nOrden = models.IntegerField('Orden', default=0, null=False)
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return "%s.- %s" % (self.nOrden, self.cIndicador)

class MedioVerificacion(models.Model):
  indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)
  cMedioVerificacion = models.CharField('Medio de Verificación', max_length=360, null=False)
  lVigente = models.BooleanField('Vigente',default=True, null=False)
  nOrden = models.IntegerField('Orden', default=0, null=False)
  dFechaMaxEntrega = models.DateField('Fecha Max Entrega', blank=True, null=True)
  oficinaResponsable = models.ForeignKey(Oficina, related_name='evidencias', on_delete=models.CASCADE, blank=True, null=True)
  idEstado = models.IntegerField('Estado', blank=True, null=True, default=1)
  usuarioCarga = models.ForeignKey(Usuario, related_name='evidencia_cargada', on_delete=models.CASCADE, blank=True, null=True)
  archivoPdf = models.FileField(upload_to='pdf/', blank=True, null=True, default='')
  dFechaCarga = models.DateTimeField('Fecha de Carga', blank=True, null=True)
  lRevisado = models.BooleanField('Revisado',default=False, null=False)
  usuarioRevisor = models.ForeignKey(Usuario, related_name='evidencia_revisada', on_delete=models.CASCADE, blank=True, null=True)
  cComentarioRevisor = models.CharField('Comentario de Revisor', max_length=360, blank=True, null=True)
  dFechaRevision = models.DateTimeField('Fecha de Revisión', blank=True, null=True)
