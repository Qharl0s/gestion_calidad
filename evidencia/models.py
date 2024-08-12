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

class Periodo(models.Model):
  class Meta:
    verbose_name_plural = "7. Periodos"
  categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, blank=True, null=True, default=1)
  cPeriodo = models.CharField('Periodo', max_length=360, default='')
  lVigente = models.BooleanField('Vigente',default=True)

  def __str__(self):
        return self.cPeriodo
  
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
  periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT, blank=True, null=True)
  
  idEstado = models.CharField('Estado', choices=ESTADO, default="Pendiente",  max_length=20)
  idEscala = models.CharField('Escala', choices=ESCALA, default="1",  max_length=120)
  usuarioCarga = models.ForeignKey(Usuario, related_name='evidencia_cargada', on_delete=models.CASCADE, blank=True, null=True)
  cDetalle1 = models.TextField('Primer Detalle', default='', blank=True, null=True,)
  cDetalle2 = models.TextField('Segundo Detalle', default='', blank=True, null=True,)
  dFechaCarga = models.DateTimeField('Fecha de Carga', blank=True, null=True)
  lFinalizado = models.BooleanField('Finalizado', default=False, null=True)
  
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
  periodo = models.ForeignKey(Periodo, on_delete=models.PROTECT, blank=True, null=True)
  
  idEstado = models.CharField('Estado', choices=ESTADO, default="Pendiente",  max_length=20)
  idEscala = models.CharField('Escala', choices=ESCALA, default="Contextualizacion",  max_length=120)
  usuarioCarga = models.ForeignKey(Usuario, related_name='evidencia_cargado', on_delete=models.CASCADE, blank=True, null=True)
  cDetalle1 = models.TextField('Primer Detalle', default='', blank=True, null=True,)
  cDetalle2 = models.TextField('Segundo Detalle', default='', blank=True, null=True,)
  dFechaCarga = models.DateTimeField('Fecha de Carga', blank=True, null=True)

class Archivo(models.Model):
  class Meta:
    verbose_name_plural = "8. Archivos"

  evidencia = models.ForeignKey(Evidencia, on_delete=models.PROTECT)
  idEscala = models.CharField('Escala', choices=ESCALA, default="Contextualizacion",  max_length=120)
  archivoPdf = models.FileField(upload_to='pdf/', blank=True, null=True, default='')
  usuario = models.ForeignKey(Usuario, related_name='evidencia_carga', on_delete=models.CASCADE, blank=True, null=True)
  dFecha = models.DateTimeField('Cargado', blank=True, null=True)
  usuarioMod = models.ForeignKey(Usuario, related_name='evidencia_actualiza', on_delete=models.CASCADE, blank=True, null=True)
  dFechaMod = models.DateTimeField('Modificado', blank=True, null=True)
  lVigente = models.BooleanField('Vigente',default=True, null=False)

class Revision(models.Model):
  class Meta:
    verbose_name_plural = "9. Revisiones"

  evidencia = models.ForeignKey(Evidencia, on_delete=models.PROTECT)
  cRevision = models.CharField('Comentario de Revisor', max_length=360, blank=True, null=True)
  idEstado = models.CharField('Estado', choices=ESTADO, default="Revisado",  max_length=20)
  dFecha = models.DateTimeField('Fecha', blank=True, null=True)
  usuario = models.ForeignKey(Usuario, related_name='evidencia_revision', on_delete=models.CASCADE, blank=True, null=True)
  lVigente = models.BooleanField('Vigente',default=True, null=False)
