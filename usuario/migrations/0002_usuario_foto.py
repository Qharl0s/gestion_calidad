# Generated by Django 3.2.5 on 2024-08-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(blank=True, default='', null=True, upload_to='foto/'),
        ),
    ]