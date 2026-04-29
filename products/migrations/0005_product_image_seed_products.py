from django.db import migrations, models


SAMPLE_PRODUCTS = [
    {
        'name': 'Wireless Headphones',
        'description': 'Comfortable over-ear wireless headphones with deep bass, soft ear cushions, and long battery life for work, travel, and everyday listening.',
        'price': '2499.00',
        'stock': 18,
        'image': 'products/wireless-headphones.png',
    },
    {
        'name': 'Smart Watch',
        'description': 'Sleek smart watch with fitness tracking, notifications, heart-rate monitoring, and an all-day strap built for daily use.',
        'price': '3499.00',
        'stock': 15,
        'image': 'products/smart-watch.png',
    },
    {
        'name': 'Travel Backpack',
        'description': 'Durable everyday backpack with padded laptop storage, front organizer pocket, side bottle space, and a clean minimalist design.',
        'price': '1799.00',
        'stock': 22,
        'image': 'products/travel-backpack.png',
    },
    {
        'name': 'Running Shoes',
        'description': 'Lightweight running shoes with breathable mesh, cushioned midsoles, and a grippy sole for walks, workouts, and casual wear.',
        'price': '2999.00',
        'stock': 20,
        'image': 'products/running-shoes.png',
    },
    {
        'name': 'Ceramic Coffee Mug',
        'description': 'Minimal ceramic coffee mug with a smooth speckled finish, comfortable handle, and sturdy build for hot drinks at home or office.',
        'price': '499.00',
        'stock': 30,
        'image': 'products/ceramic-mug.png',
    },
]


def seed_sample_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')

    for product in SAMPLE_PRODUCTS:
        Product.objects.update_or_create(
            name=product['name'],
            defaults={
                'description': product['description'],
                'price': product['price'],
                'stock': product['stock'],
                'image': product['image'],
            },
        )


def remove_sample_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Product.objects.filter(name__in=[product['name'] for product in SAMPLE_PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
        migrations.RunPython(seed_sample_products, remove_sample_products),
    ]
