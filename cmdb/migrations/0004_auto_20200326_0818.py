# Generated by Django 3.0.4 on 2020-03-26 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_application_hosttoapp'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='r',
            field=models.ManyToManyField(to='cmdb.Host'),
        ),
        migrations.DeleteModel(
            name='HostToApp',
        ),
    ]
