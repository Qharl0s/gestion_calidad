# Generated by Django 3.2.5 on 2024-08-20 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_usuario_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='lRevisor',
            field=models.BooleanField(default=False, null=True, verbose_name='Revisor'),
        ),
    ]