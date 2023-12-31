# Generated by Django 4.2.8 on 2024-01-08 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=25)),
                ('description', models.TextField(max_length=75)),
                ('count', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('category', models.ManyToManyField(to='labels.categorygame')),
                ('compatibility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labels.modelconsole')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labels.developer')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labels.status')),
            ],
        ),
        migrations.CreateModel(
            name='Console',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=25)),
                ('description', models.TextField(max_length=75)),
                ('count', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('model_console', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labels.modelconsole')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labels.status')),
            ],
        ),
    ]
