# Generated by Django 2.1.7 on 2019-06-25 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cil', '0008_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.CharField(default='guest', max_length=10),
            preserve_default=False,
        ),
    ]
