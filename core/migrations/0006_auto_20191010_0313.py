# Generated by Django 2.2.5 on 2019-10-10 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_ticket_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='estimated',
            field=models.DurationField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='reported',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
