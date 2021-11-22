# Generated by Django 3.2 on 2021-05-20 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_auto_20210520_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterparties',
            name='term_of_contract',
            field=models.DateTimeField(verbose_name='Срок договора'),
        ),
        migrations.AlterField(
            model_name='educatedwaste',
            name='date_of_educated',
            field=models.DateTimeField(verbose_name='Дата образования'),
        ),
        migrations.AlterField(
            model_name='reclaimedwaste',
            name='date_of_reclaimed',
            field=models.DateTimeField(verbose_name='Дата образования'),
        ),
        migrations.AlterField(
            model_name='transferredwaste',
            name='date_of_transferred',
            field=models.DateTimeField(verbose_name='Дата образования'),
        ),
    ]
