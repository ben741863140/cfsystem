# Generated by Django 2.2.7 on 2019-12-11 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logreg', '0003_captcha'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.IntegerField(choices=[(1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'), (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52'), (53, '53'), (54, '54'), (55, '55'), (56, '56'), (57, '57'), (58, '58'), (59, '59'), (60, '60'), (61, '61'), (62, '62'), (63, '63'), (64, '64'), (65, '65'), (66, '66'), (67, '67'), (68, '68'), (69, '69'), (70, '70'), (71, '71'), (72, '72'), (73, '73'), (74, '74'), (75, '75'), (76, '76'), (77, '77'), (78, '78'), (79, '79'), (80, '80'), (81, '81'), (82, '82'), (83, '83'), (84, '84'), (85, '85'), (86, '86'), (87, '87'), (88, '88'), (89, '89'), (90, '90'), (91, '91'), (92, '92'), (93, '93'), (94, '94'), (95, '95'), (96, '96'), (97, '97'), (98, '98')], default=16, error_messages={'blank': '不能为空'}, help_text='<ul><li>必填</li></ul>', verbose_name='年级'),
        ),
        migrations.AddField(
            model_name='user',
            name='oj_password',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
