"""
Script to add W203 product (Girls Set)
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
    print("ERROR: Sizes 4, 6, 8, 10 not found.")
    exit(1)

# 3. Create Product W203
product, created = Product.objects.get_or_create(
    slug='disneyland-california-ribbon-set-w203',
    defaults={
        'name': 'Disneyland California Ribbon Set W203',
        'description': 'Adorable girls sweatshirt set featuring a vibrant "Disneyland California" print with Mickey, Minnie, Goofy, and Pluto. Unique ribbon lace-up details on the sides of the sleeves and pants add a stylish touch. Comfortable and fun for any outing.',
        'category': category,
        'base_price': Decimal('560.00'),
        'main_image': 'products/W203/skyblue.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# 4. Define colors
color_data = [
    {'name': 'Sky Blue', 'hex': '#87CEEB', 'img': 'skyblue.jpg'}, # Image 0
    {'name': 'Lime Green', 'hex': '#32CD32', 'img': 'lime.jpg'},  # Image 1
    {'name': 'Hot Pink', 'hex': '#FF69B4', 'img': 'pink.jpg'},   # Image 2
    {'name': 'Lavender', 'hex': '#E6E6FA', 'img': 'lavender.jpg'}, # Image 3
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
    img_path = f'products/W203/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path}")

print(f"\n[SUCCESS] Product W203 added to 'Girls Set' category!")
