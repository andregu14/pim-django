# Generated by Django 5.1.1 on 2024-10-15 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinicaMedica', '0013_alter_consulta_data_hora_alter_dentista_cro'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consulta',
            unique_together={('data_hora', 'medico_dentista')},
        ),
    ]