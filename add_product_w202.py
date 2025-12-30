"""
Script to add W202 product (Girls Set)
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# 1. Get category "Girls Set"
category = Category.objects.get(slug='girls-set')

# 2. Get sizes 4, 6, 8, 10
sizes_to_use = []
for size_name in ['4', '6', '8', '10']:
    size = Size.objects.filter(name=size_name).first()
    if size:
        sizes_to_use.append(size)

if not sizes_to_use:
    print("ERROR: Sizes 4, 6, 8, 10 not found. Run W200 script first.")
    exit(1)

# 3. Create Product W202
product, created = Product.objects.get_or_create(
    slug='good-day-daisy-set-w202',
    defaults={
        'name': 'Good Day Daisy Set W202',
        'description': 'Beautiful girls set featuring a puff-sleeve hoodie with a sequin daisy design and "Today is a Good Day" slogan. Paired with comfortable wide-leg sweatpants. Stylish, positive, and perfect for special occasions or daily wear.',
        'category': category,
        'base_price': Decimal('550.00'),
        'main_image': 'products/W202/cream.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# 4. Define colors
color_data = [
    {'name': 'Cream & Coral', 'hex': '#FFFDD0,#FF7F50', 'img': 'cream.jpg'}, # Image 0
    {'name': 'Lavender & Black', 'hex': '#E6E6FA,#000000', 'img': 'lavender.jpg'}, # Image 1
    {'name': 'Mustard & Magenta', 'hex': '#FFDB58,#8B008B', 'img': 'mustard.jpg'}, # Image 2
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
    
    for size in sizes_to_use:
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
                defaults={'quantity': 15}
            )
    
    # Link Image
    img_path = f'products/W202/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path}")

print(f"\n[SUCCESS] Product W202 added to 'Girls Set' category!")
