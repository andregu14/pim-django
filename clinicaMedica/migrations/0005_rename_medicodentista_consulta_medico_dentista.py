# Generated by Django 5.1.1 on 2024-09-17 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinicaMedica', '0004_paciente_cpf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consulta',
            old_name='MedicoDentista',
            new_name='medico_dentista',
        ),
    ]