# Generated by Django 5.1.6 on 2025-02-12 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_customer_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Complete', 'Complete'), ('Failed', 'Failed')], default='Pending', max_length=8),
        ),
    ]
