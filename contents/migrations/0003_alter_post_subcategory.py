# Generated by Django 4.0.2 on 2022-06-09 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0002_remove_subcategory_post_post_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contents.subcategory'),
        ),
    ]
