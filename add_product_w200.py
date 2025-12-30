"""
Script to add W200 product, new category 'Girls Set', and toddler sizes
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product, Color, Size, ProductVariant, Stock, Store, ProductImage

# 1. Create new category "Girls Set"
category, cat_created = Category.objects.get_or_create(
    slug='girls-set',
    defaults={'name': 'Girls Set'}
)
if cat_created:
    print(f"[OK] Created Category: {category.name}")
else:
    print(f"[OK] Category exists: {category.name}")

# 2. Add new sizes: 4, 6, 8, 10
# Assuming order fills gap between 1-3 (baby) and 12-18 (teen)
# Baby sizes (1,2,3) might have order 1,2,3. Teen sizes have 100+.
# Let's set order 50+ to be safe and distinct.
new_sizes = ['4', '6', '8', '10']
created_sizes = []
for i, size_name in enumerate(new_sizes):
    order = 50 + i 
    size, created = Size.objects.get_or_create(
        name=size_name,
        defaults={'order': order}
    )
    if created:
        print(f"  [OK] Created Size: {size.name}")
    created_sizes.append(size)

# 3. Create Product W200
product, created = Product.objects.get_or_create(
    slug='dont-worry-be-happy-set-w200',
    defaults={
        'name': 'Don\'t Worry Be Happy Set W200',
        'description': 'Cheerful "Don\'t Worry Be Happy" hoodie set featuring a smiley bunny design and matching joggers. Vibrant colors and fun prints make this a favorite for little girls. Soft, comfortable fabric perfect for play.',
        'category': category,
        'base_price': Decimal('550.00'),
        'main_image': 'products/W200/blue_main.jpg',
        'is_active': True
    }
)

if created:
    print(f"[OK] Created product: {product.name}")
else:
    print(f"[OK] Product already exists: {product.name}")

# 4. Define colors
color_data = [
    {'name': 'Light Blue & Dark Pink', 'hex': '#ADD8E6,#C71585', 'img': 'blue_main.jpg'},
    {'name': 'Pink & Dark Pink', 'hex': '#FFC0CB,#C71585', 'img': 'pink.jpg'},
    {'name': 'Lavender & Black', 'hex': '#E6E6FA,#000000', 'img': 'lavender.jpg'},
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
                defaults={'quantity': 15}
            )
    
    # Link Image
    img_path = f'products/W200/{color_info["img"]}'
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=img_path,
        defaults={'alt_text': f'{color.name} variant', 'color': color}
    )
    if img_created:
        print(f"[OK] Added image: {img_path}")

print(f"\n[SUCCESS] Product W200 added to 'Girls Set' category!")
