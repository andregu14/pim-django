# Generated by Django 5.1.1 on 2024-10-15 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicaMedica', '0010_servico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='nome',
            field=models.CharField(max_length=40, verbose_name='Serviço'),
        ),
    ]
