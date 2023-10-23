from django.db import models
from usuario.models import Usuario, Oficina

class Categoria(models.Model):
  class Meta:
    verbose_name_plural = "1. Categorias"
  cCategoria = models.CharField('Categoria', max_length=360, default='')
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cCategoria

class Grupo(models.Model):
  class Meta:
    verbose_name_plural = "2. Grupos"
  categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
  cGrupo = models.CharField('Grupo', max_length=360, default='')
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cGrupo

class Indicador(models.Model):
  class Meta:
    verbose_name_plural = "3. Indicadores"
  grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
  cTitulo = models.CharField('Titulo', max_length=120, default='')
  cIndicador = models.CharField('Indicador', max_length=360, default='')
  cDescripcion = models.CharField('Descripción', max_length=360, default='')
  nOrden = models.IntegerField('Orden', default=0, null=False)
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cTitulo

class MedioVerificacion(models.Model):
  class Meta:
    verbose_name_plural = "4. Medios de Verficación"
  indicador = models.ForeignKey(Indicador, on_delete=models.PROTECT)
  cTitulo = models.CharField('Titulo', max_length=500, default='')
  cMedioVerificacion = models.CharField('Medio de Verificación', max_length=700, null=False)
  nOrden = models.IntegerField('Orden', default=0, null=False)
  dFechaMaxEntrega = models.DateField('Fecha Max Entrega', blank=True, null=True)
  oficinaResponsable = models.ForeignKey(Oficina, related_name='evidencias', on_delete=models.CASCADE, blank=True, null=True)
  lVigente = models.BooleanField('Vigente',default=True, null=False)

ESTADO = (
    ('Pendiente', 'Pendiente'),
    ('Cargado', 'Cargado'),
    ('Revisado', 'Revisado'),
    ('Observado', 'Observado'),
    ('Aprobado', 'Aprobado'),
  )
  
ESCALA = (
  ('1', 'Contextualización'),
  ('2', 'Planificación'),
  ('3', 'Optimización'),
  ('4', 'Avance de actividades al 25%'),
  ('5', 'Avance de actividades al 50%'),
  ('6', 'Avance de actividades al 75%'),
  ('7', 'Avance de actividades al 100%'),
  ('8', 'Análisis de resultados'),
  ('9', 'Justificación'),
  ('10', 'Finalizado'),
)
  
class Evidencia(models.Model):
  class Meta:
    verbose_name_plural = "5. Evidencias"
  
  
  medioVerificacion = models.ForeignKey(MedioVerificacion, on_delete=models.CASCADE, blank=True, null=True)
  oficina = models.ForeignKey(Oficina, related_name='oficina', on_delete=models.CASCADE, blank=True, null=True)
  
  idEstado = models.CharField('Estado', choices=ESTADO, default="Pendiente",  max_length=20)
  idEscala = models.CharField('Escala', choices=ESCALA, default="1",  max_length=120)
  usuarioCarga = models.ForeignKey(Usuario, related_name='evidencia_cargada', on_delete=models.CASCADE, blank=True, null=True)
  cDetalle1 = models.TextField('Primer Detalle', default='', blank=True, null=True,)
  cDetalle2 = models.TextField('Segundo Detalle', default='', blank=True, null=True,)
  archivoPdf = models.FileField(upload_to='pdf/', blank=True, null=True, default='')
  dFechaCarga = models.DateTimeField('Fecha de Carga', blank=True, null=True)
  lRevisado = models.BooleanField('Revisado',default=False, null=False)
  usuarioRevisor = models.ForeignKey(Usuario, related_name='evidencia_revisada', on_delete=models.CASCADE, blank=True, null=True)
  cComentarioRevisor = models.CharField('Comentario de Revisor', max_length=360, blank=True, null=True)
  dFechaRevision = models.DateTimeField('Fecha de Revisión', blank=True, null=True)
  
  def escala_desc(self):
    d = dict(ESCALA)
    if self.idEscala in d:
        return d[self.idEscala]
    return None

  
class Evidencia_Todo(models.Model):
  class Meta:
    verbose_name_plural = "6. Evidencias Todo"
  
  medioVerificacion = models.ForeignKey(MedioVerificacion, on_delete=models.CASCADE, blank=True, null=True)
  oficina = models.ForeignKey(Oficina, related_name='oficinas', on_delete=models.CASCADE, blank=True, null=True)
  
  idEstado = models.CharField('Estado', choices=ESTADO, default="Pendiente",  max_length=20)
  idEscala = models.CharField('Escala', choices=ESCALA, default="Contextualizacion",  max_length=120)
  usuarioCarga = models.ForeignKey(Usuario, related_name='evidencia_cargado', on_delete=models.CASCADE, blank=True, null=True)
  cDetalle1 = models.TextField('Primer Detalle', default='', blank=True, null=True,)
  cDetalle2 = models.TextField('Segundo Detalle', default='', blank=True, null=True,)
  archivoPdf = models.FileField(upload_to='pdf/', blank=True, null=True, default='')
  dFechaCarga = models.DateTimeField('Fecha de Carga', blank=True, null=True)
  lRevisado = models.BooleanField('Revisado',default=False, null=False)
  usuarioRevisor = models.ForeignKey(Usuario, related_name='evidencia_revisado', on_delete=models.CASCADE, blank=True, null=True)
  cComentarioRevisor = models.CharField('Comentario de Revisor', max_length=360, blank=True, null=True)
  dFechaRevision = models.DateTimeField('Fecha de Revisión', blank=True, null=True)