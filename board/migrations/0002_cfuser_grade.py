# Generated by Django 2.2.7 on 2019-12-11 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cfuser',
            name='grade',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
