# Generated by Django 4.1.1 on 2023-01-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_variantoption_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='variantoption',
            name='unique_variant_option_name',
        ),
        migrations.AddConstraint(
            model_name='variantoption',
            constraint=models.UniqueConstraint(fields=('name', 'product'), name='unique_variant_option_name_product'),
        ),
    ]