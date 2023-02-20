# Generated by Django 4.1.6 on 2023-02-20 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0006_remove_order_jewelry_remove_order_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='workshop.OrderItem', to='workshop.jewelry'),
        ),
    ]
