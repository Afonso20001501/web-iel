# Generated by Django 5.0.6 on 2024-06-25 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webiel', '0007_alter_noticia_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='BancoDeAlimentacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=65)),
                ('telefone', models.IntegerField()),
                ('bairro', models.CharField(max_length=255)),
                ('donativo', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'BancoDelimentacao',
            },
        ),
        migrations.CreateModel(
            name='Carta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=65)),
                ('destino', models.CharField(max_length=255)),
                ('objectivo', models.CharField(max_length=255)),
                ('tipo_carta', models.CharField(max_length=255)),
                ('telefone', models.IntegerField()),
                ('outras_inf', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Cartas',
            },
        ),
        migrations.CreateModel(
            name='Casamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_noivo', models.CharField(max_length=255)),
                ('nome_noiva', models.CharField(max_length=255)),
                ('telefone', models.IntegerField()),
                ('data_casam', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Casamentos',
            },
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=65)),
                ('telefone', models.IntegerField()),
                ('mensagem', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Mensagens',
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=65)),
            ],
            options={
                'verbose_name_plural': 'Newsletter',
            },
        ),
    ]
