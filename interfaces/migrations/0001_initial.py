# Generated by Django 2.2.7 on 2019-12-14 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OJUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('is_super', models.BooleanField(default=False)),
                ('cf_handle', models.CharField(blank=True, max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
