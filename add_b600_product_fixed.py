"""
Script to add B600 product to the database
Run with: python manage.py shell -c "exec(open('add_b600_product_fixed.py').read())"
"""

from store.models import Category, Product, Color, Size, ProductVariant, ProductImage, Stock, Store
from decimal import Decimal

# Get or create category
category, _ = Category.objects.get_or_create(
    slug='baby-sets',
    defaults={'name': 'Baby Sets'}
)

# Create product
product, created = Product.objects.get_or_create(
    slug='cozy-day-baby-set-b600',
    defaults={
        'name': 'Cozy Day Baby Set - B600',
        'description': 'Adorable "Have a Cozy Day" themed baby outfit set featuring a comfortable sweatshirt with cute character print and matching ruffled pants. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort. Each set includes a long-sleeve top with shoulder ruffles and coordinating pants with decorative ruffle details.',
        'category': category,
        'base_price': Decimal('450.00'),
        'main_image': 'products/B600/white_pink.jpg',
        'is_active': True
    }
)

if created:
    print(f"✓ Created product: {product.name}")
else:
    print(f"✓ Product already exists: {product.name}")

# Define colors and their image files
color_data = [
    {'name': 'White & Pink', 'hex': '#FFB6C1', 'image': 'products/B600/white_pink.jpg'},
    {'name': 'Orange & Lavender', 'hex': '#FFA07A', 'image': 'products/B600/orange_lavender.jpg'},
    {'name': 'Yellow & Turquoise', 'hex': '#FFD700', 'image': 'products/B600/yellow_turquoise.jpg'},
]

# Define sizes for B series
size_data = [
    {'name': '1', 'order': 1},
    {'name': '2', 'order': 2},
    {'name': '3', 'order': 3},
]

# Get or create default store
store, _ = Store.objects.get_or_create(
    name="Main Store",
    defaults={'address': 'Cairo, Egypt', 'is_active': True}
)

# Create colors, sizes, variants, and stock
for color_info in color_data:
    color, _ = Color.objects.get_or_create(
        name=color_info['name'],
        defaults={'hex_code': color_info['hex']}
    )
    
    for size_info in size_data:
        size, _ = Size.objects.get_or_create(
            name=size_info['name'],
            defaults={'order': size_info['order']}
        )
        
        # Create variant
        variant, variant_created = ProductVariant.objects.get_or_create(
            product=product,
            color=color,
            size=size,
            defaults={'sku': f"B600-{color.name[:3].upper()}-{size.name}"}
        )
        
        if variant_created:
            print(f"  ✓ Created variant: {color.name} - Size {size.name}")
            
            # Add stock
            Stock.objects.get_or_create(
                variant=variant,
                store=store,
                defaults={'quantity': 10}
            )
    
    # Add product image to gallery
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        image=color_info['image'],
        defaults={
            'alt_text': f"Cozy Day Baby Set - {color.name}"
        }
    )
    
    if img_created:
        print(f"  ✓ Added image for {color.name}")

print(f"\n✅ Product B600 successfully added with {len(color_data)} colors and {len(size_data)} sizes!")
print(f"Total variants created: {len(color_data) * len(size_data)}")
