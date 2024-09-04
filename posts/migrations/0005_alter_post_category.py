# Generated by Django 3.2.23 on 2024-09-04 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_category_options'),
        ('posts', '0004_auto_20240904_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category'),
        ),
    ]
