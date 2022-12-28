# Generated by Django 3.2.14 on 2022-12-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0034_alter_celerytask_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaljob',
            name='module',
            field=models.CharField(choices=[('shell', 'Shell'), ('win_shell', 'Powershell'), ('python', 'Python')], default='shell', max_length=128, null=True, verbose_name='Module'),
        ),
        migrations.AlterField(
            model_name='historicaljob',
            name='timeout',
            field=models.IntegerField(default=-1, verbose_name='Timeout (Seconds)'),
        ),
        migrations.AlterField(
            model_name='job',
            name='module',
            field=models.CharField(choices=[('shell', 'Shell'), ('win_shell', 'Powershell'), ('python', 'Python')], default='shell', max_length=128, null=True, verbose_name='Module'),
        ),
        migrations.AlterField(
            model_name='job',
            name='timeout',
            field=models.IntegerField(default=-1, verbose_name='Timeout (Seconds)'),
        ),
    ]