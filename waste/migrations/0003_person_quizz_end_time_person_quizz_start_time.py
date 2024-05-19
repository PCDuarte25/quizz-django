# Generated by Django 5.0.6 on 2024-05-19 18:01

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0002_alter_person_options_person_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='quizz_end_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 19, 15, 0, 43, 554761), verbose_name='horário que terminou o quizz'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='quizz_start_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='horário que começou o quizz'),
            preserve_default=False,
        ),
    ]
