# Generated by Django 4.2.8 on 2024-01-11 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_alter_console_description_alter_game_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallerygame',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='goods.game'),
        ),
    ]
