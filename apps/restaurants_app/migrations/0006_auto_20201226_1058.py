# Generated by Django 2.2.4 on 2020-12-26 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants_app', '0005_auto_20201225_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='description',
            field=models.CharField(max_length=97),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.User'),
        ),
    ]
