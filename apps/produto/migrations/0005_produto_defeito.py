# Generated by Django 5.1.6 on 2025-02-23 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_produto_responsavel_conserto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='defeito',
            field=models.CharField(choices=[('1', 'SEM DEFEITO'), ('2', 'ESTÉTICO'), ('3', 'ESTÉTICO-FUNCIONAL'), ('4', 'FUNCIONAL'), ('5', 'VENDA DIRETA')], default='1', max_length=30),
        ),
    ]
