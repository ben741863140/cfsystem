# Generated by Django 2.0.1 on 2018-04-25 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('effective_time', models.DateTimeField(default=0)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BoardItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_rating', models.IntegerField()),
                ('oldRating', models.IntegerField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.Board')),
            ],
        ),
        migrations.CreateModel(
            name='CFUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=30, unique=True)),
                ('rating', models.IntegerField(default=0)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('realname', models.CharField(default='', max_length=5)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RatingChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days_ago', models.IntegerField(null=True)),
                ('oldRating', models.IntegerField(default=0)),
                ('newRating', models.IntegerField(default=0)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('ratingUpdateTimeSeconds', models.IntegerField(null=True)),
                ('cf_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.CFUser')),
            ],
        ),
        migrations.AddField(
            model_name='boarditem',
            name='cf_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='board.CFUser'),
        ),
    ]
