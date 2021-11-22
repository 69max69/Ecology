# Generated by Django 3.2 on 2021-05-17 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nameofbranch',
            options={'ordering': ['pk'], 'verbose_name': 'Филиал', 'verbose_name_plural': 'Филиалы'},
        ),
        migrations.AlterModelOptions(
            name='nameofobjects',
            options={'ordering': ['pk'], 'verbose_name': 'Объект', 'verbose_name_plural': 'Объекты'},
        ),
        migrations.AlterModelOptions(
            name='waste',
            options={'ordering': ['number'], 'verbose_name': 'Отход', 'verbose_name_plural': 'Отходы'},
        ),
        migrations.AddField(
            model_name='educatedwaste',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.nameofbranch', verbose_name='Филиал'),
        ),
        migrations.AddField(
            model_name='reclaimedwaste',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.nameofbranch', verbose_name='Филиал'),
        ),
        migrations.AddField(
            model_name='transferredwaste',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='accounting.nameofbranch', verbose_name='Филиал'),
        ),
    ]