# Generated by Django 4.1.3 on 2024-01-09 23:00

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_productinfo_description_alter_order_delivery_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productparameter',
            options={'verbose_name': 'Параметр', 'verbose_name_plural': 'Параметры товара'},
        ),
        migrations.AddField(
            model_name='order',
            name='recipient_full_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='ФИО получателя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, default=datetime.date(2024, 1, 11), null=True, validators=[django.core.validators.MinValueValidator(datetime.date(2024, 1, 11))], verbose_name='Дата доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(blank=True, choices=[('morning_09_12', '09:00 - 12:00'), ('afternoon_12_15', '12:00 - 15:00'), ('afternoon_15_18', '15:00 - 18:00'), ('evening_18_22', '18:00 - 22:00')], default='morning_09_12', max_length=30, null=True, verbose_name='Время доставки'),
        ),
    ]
