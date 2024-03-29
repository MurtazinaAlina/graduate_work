# Generated by Django 4.1.3 on 2023-12-29 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(blank=True, choices=[('morning', '09:00 - 12:00'), ('afternoon_12', '12:00 - 15:00'), ('afternoon_15', '15:00 - 18:00'), ('evening', '18:00 - 22:00')], default='morning', max_length=30, null=True, verbose_name='Время доставки'),
        ),
    ]
