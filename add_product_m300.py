"""
Script to add M300 product, new category, and teen sizes
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# 1. Create new category "Boys Set"
category, cat_created = Category.objects.get_or_create(
    slug='boys-set',
    defaults={'name': 'Boys Set'}
)
if cat_created:
    print(f"[OK] Created Category: {category.name}")
else:
    print(f"[OK] Category exists: {category.name}")

# 2. Add new sizes: 12, 14, 16, 18
new_sizes = ['12', '14', '16', '18']
created_sizes = []
for i, size_name in enumerate(new_sizes):
    # Setting order higher than baby sizes (usually > 100)
    order = 100 + i 
    size, created = Size.objects.get_or_create(
        name=size_name,
        defaults={'order': order}
    )
    if created:
        print(f"  [OK] Created Size: {size.name}")
    created_sizes.append(size)

# 3. Create Product M300
product, created = Product.objects.get_or_create(
    slug='pro-sport-tracksuit-m300',
    defaults={
        'name': 'Pro Sport Tracksuit M300',
        'description': 'Premium athletic tracksuit set taking inspiration from top football clubs. Features a comfortable hoodie with sporty color-block design and matching joggers. Perfect for active boys and teens. Made with high-quality, durable fabric.',
        'category': category,
        'base_price': Decimal('650.00'), # Higher price point for older kids/teens
        'main_image': 'products/M300/white_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# 4. Define colors
color_data = [
    {'name': 'White & Black', 'hex': '#FFFFFF,#000000', 'img': 'white_main.jpg'},
    {'name': 'Charcoal & Blue', 'hex': '#36454F,#1E90FF', 'img': 'charcoal.jpg'},
    {'name': 'Pink & Blue', 'hex': '#FFC0CB,#87CEFA', 'img': 'pink.jpg'},
]

# Get or create default store
store, _ = Store.objects.get_or_create(
    name="Main Store",
    defaults={'address': 'Cairo, Egypt'}
)

# 5. Create variants and stock
for color_info in color_data:
    color, color_created = Color.objects.get_or_create(
        name=color_info['name'],
        defaults={'hex_code': color_info['hex']}
    )
    
    if color_created:
        print(f"  [OK] Created color: {color.name}")
    
    for size in created_sizes:
        variant, variant_created = ProductVariant.objects.get_or_create(
            product=product,
            color=color,
            size=size,
            defaults={'additional_price': Decimal('0.00')}
        )
        
        if variant_created:
            print(f"    [OK] Created {color.name} - Size {size.name}")
            Stock.objects.get_or_create(
                variant=variant,
                store=store,
                defaults={'quantity': 10}
            )
    
    # Link Image
    img_path = f'products/M300/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path}")

print(f"\n[SUCCESS] Product M300 added to 'Boys Set' category!")
