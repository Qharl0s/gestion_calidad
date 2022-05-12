# Generated by Django 3.2.5 on 2022-05-10 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evidencia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidencia',
            name='idEscala',
            field=models.CharField(choices=[('1', 'Contextualización'), ('2', 'Planificación'), ('3', 'Optimización'), ('3', 'Avance de actividades al 25%'), ('4', 'Avance de actividades al 50%'), ('5', 'Avance de actividades al 75%'), ('6', 'Avance de actividades al 100%'), ('7', 'Análisis de resultados'), ('8', 'Justificación'), ('9', 'Finalizado')], default='Contextualizacion', max_length=120, verbose_name='Escala'),
        ),
        migrations.AlterField(
            model_name='evidencia',
            name='medioVerificacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evidencia.medioverificacion'),
        ),
    ]
