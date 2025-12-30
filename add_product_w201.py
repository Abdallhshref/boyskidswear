"""
Script to add W201 product (Unisex/Kids)
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# 1. Create new category "Kids Sets" (Since this product has both boys and girls)
category, cat_created = Category.objects.get_or_create(
    slug='kids-sets',
    defaults={'name': 'Kids Sets'}
)
if cat_created:
    print(f"[OK] Created Category: {category.name}")
else:
    print(f"[OK] Category exists: {category.name}")

# 2. Get sizes 4, 6, 8, 10 (Created in W200)
sizes_to_use = []
for size_name in ['4', '6', '8', '10']:
    size = Size.objects.filter(name=size_name).first()
    if size:
        sizes_to_use.append(size)

if not sizes_to_use:
    print("ERROR: Sizes 4, 6, 8, 10 not found. Run W200 script first.")
    exit(1)

# 3. Create Product W201
product, created = Product.objects.get_or_create(
    slug='pilot-color-block-set-w201',
    defaults={
        'name': 'Pilot Color Block Set W201',
        'description': 'Trendy color-block hoodie set featuring the distinct "THE PILOT" patch. Available in a variety of vibrant and neutral combinations for both boys and girls. Includes a comfy hoodie with kangaroo pocket and matching joggers. Durable and stylish.',
        'category': category,
        'base_price': Decimal('580.00'),
        'main_image': 'products/W201/beige.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# 4. Define colors
# Mapping images to colors based on input
color_data = [
    {'name': 'Beige & Black', 'hex': '#F5F5DC,#000000', 'img': 'beige.jpg'}, # From image 0
    {'name': 'Hot Pink & White', 'hex': '#FF69B4,#FFFFFF', 'img': 'hot_pink.jpg'}, # From image 0
    {'name': 'Black & Pink', 'hex': '#000000,#FFC0CB', 'img': 'black_pink.jpg'}, # From image 1
    {'name': 'Salmon & Navy', 'hex': '#FA8072,#000080', 'img': 'salmon.jpg'}, # From image 1/3
    {'name': 'Blue & Red', 'hex': '#4169E1,#FF0000', 'img': 'blue.jpg'}, # From image 2
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
    img_path = f'products/W201/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path}")

print(f"\n[SUCCESS] Product W201 added to 'Kids Sets' category!")
