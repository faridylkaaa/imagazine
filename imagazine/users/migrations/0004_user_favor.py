# Generated by Django 4.2.8 on 2024-01-17 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('users', '0003_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favor',
            field=models.ManyToManyField(blank=True, null=True, related_name='user', to='goods.goods'),
        ),
    ]
