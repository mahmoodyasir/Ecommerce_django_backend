# Generated by Django 4.0 on 2021-12-25 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_choice_alter_order_order_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_status',
        ),
        migrations.AddField(
            model_name='order',
            name='order_list',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='shop.choice'),
        ),
    ]
