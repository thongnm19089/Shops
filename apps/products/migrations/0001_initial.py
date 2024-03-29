# Generated by Django 4.1.1 on 2023-01-02 01:04

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'brand',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('color', models.CharField(blank=True, max_length=20, null=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('landing_page_position', models.PositiveIntegerField(blank=True, null=True)),
                ('landing_page_active', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'db_table': 'category',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('ascii_name', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.PositiveIntegerField()),
                ('barcode', models.CharField(blank=True, max_length=20, null=True)),
                ('sku', models.CharField(blank=True, max_length=20, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('position', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('landing_page_position', models.PositiveIntegerField(blank=True, null=True)),
                ('landing_page_active', models.BooleanField(blank=True, default=False, null=True)),
                ('landing_page_show_price', models.BooleanField(default=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.brand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.category')),
            ],
            options={
                'db_table': 'product',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=100)),
                ('image_url', models.FileField(max_length=1024, upload_to=core.models.UploadTo('shops', 'product'))),
                ('size', models.IntegerField()),
                ('position', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_exported', models.BooleanField()),
                ('reason', models.CharField(choices=[('E_USED', 'E_USED'), ('E_DAMAGED', 'E_DAMAGED'), ('E_OUTDATED', 'E_OUTDATED'), ('E_LOSS', 'E_LOSS'), ('I_NEW', 'I_NEW'), ('I_RETURN', 'I_RETURN'), ('I_TRANSFER', 'I_TRANSFER'), ('OTHER', 'OTHER'), ('ADJUST', 'ADJUST')], max_length=30)),
                ('current_total', models.IntegerField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shops.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inventory_history', to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='inventory_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inventory_history',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='shops.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'db_table': 'inventory',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_category_name'),
        ),
        migrations.AddConstraint(
            model_name='brand',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_brand_name'),
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_product_name'),
        ),
    ]
