# Generated by Django 4.2.8 on 2024-01-05 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(blank=True, null=True),
        ),
    ]
