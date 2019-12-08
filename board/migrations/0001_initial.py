# Generated by Django 2.2 on 2019-12-08 15:51

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
            name='RatingChange',
            fields=[
                ('newRating', models.IntegerField()),
                ('ratingUpdateTimeSeconds', models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'board_ratingchange',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('type', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
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
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BoardItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_rating', models.IntegerField()),
                ('old_rating', models.IntegerField()),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('times', models.IntegerField(default=0)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.Board')),
                ('cf_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='board.CFUser')),
            ],
        ),
    ]