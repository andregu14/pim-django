# Generated by Django 5.1.1 on 2024-10-14 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinicaMedica', '0005_alter_dentista_periodo_trabalho'),
    ]

    operations = [
        migrations.AddField(
            model_name='dentista',
            name='cro',
            field=models.CharField(default=123, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
