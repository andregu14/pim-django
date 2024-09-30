# Generated by Django 5.1.1 on 2024-09-17 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicaMedica', '0002_gestor_senha_medicodentista_senha_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id_consulta', models.AutoField(primary_key=True, serialize=False)),
                ('data_hora', models.DateTimeField(verbose_name='Data e Hora')),
                ('status', models.CharField(max_length=20)),
                ('MedicoDentista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinicaMedica.medicodentista')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinicaMedica.paciente')),
            ],
        ),
    ]
