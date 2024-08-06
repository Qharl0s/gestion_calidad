# Generated by Django 3.2.5 on 2024-07-23 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evidencia', '0011_auto_20240617_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evidencia',
            name='cComentarioRevisor',
        ),
        migrations.RemoveField(
            model_name='evidencia',
            name='dFechaRevision',
        ),
        migrations.RemoveField(
            model_name='evidencia',
            name='lRevisado',
        ),
        migrations.RemoveField(
            model_name='evidencia',
            name='usuarioRevisor',
        ),
        migrations.RemoveField(
            model_name='evidencia_todo',
            name='cComentarioRevisor',
        ),
        migrations.RemoveField(
            model_name='evidencia_todo',
            name='dFechaRevision',
        ),
        migrations.RemoveField(
            model_name='evidencia_todo',
            name='lRevisado',
        ),
        migrations.RemoveField(
            model_name='evidencia_todo',
            name='usuarioRevisor',
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cRevision', models.CharField(blank=True, max_length=360, null=True, verbose_name='Comentario de Revisor')),
                ('idEstado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Cargado', 'Cargado'), ('Revisado', 'Revisado'), ('Observado', 'Observado'), ('Aprobado', 'Aprobado')], default='Revisado', max_length=20, verbose_name='Estado')),
                ('dFecha', models.DateTimeField(blank=True, null=True, verbose_name='Fecha')),
                ('lVigente', models.BooleanField(default=True, verbose_name='Vigente')),
                ('evidencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='evidencia.evidencia')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evidencia_revision', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '9. Revisiones',
            },
        ),
    ]
