"""
Script to add B600 product to the database
Run with: python manage.py shell < add_b600_product.py
"""

from store.models import Category, Product, Color, Size, ProductVariant, ProductImage, Stock, Store
from decimal import Decimal

# Get or create category
category, _ = Category.objects.get_or_create(
    name="Baby Sets",
    defaults={'slug': 'baby-sets'}
)

# Create product
product, created = Product.objects.get_or_create(
    code="B600",
    defaults={
        'name': 'Cozy Day Baby Set',
        'slug': 'cozy-day-baby-set-b600',
        'description': 'Adorable "Have a Cozy Day" themed baby outfit set featuring a comfortable sweatshirt with cute character print and matching pants. Perfect for everyday wear, playtime, or casual outings. Made with soft, breathable fabric for your little one\'s comfort.',
        'category': category,
        'price': Decimal('450.00'),
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
size_values = ['1', '2', '3']

# Get or create default store
store, _ = Store.objects.get_or_create(
    name="Main Store",
    defaults={'location': 'Cairo'}
)

# Create colors, sizes, variants, and stock
for color_info in color_data:
    color, _ = Color.objects.get_or_create(
        name=color_info['name'],
        defaults={'hex_code': color_info['hex']}
    )
    
    for size_val in size_values:
        size, _ = Size.objects.get_or_create(value=size_val)
        
        # Create variant
        variant, variant_created = ProductVariant.objects.get_or_create(
            product=product,
            color=color,
            size=size,
            defaults={'sku': f"B600-{color.name[:3].upper()}-{size_val}"}
        )
        
        if variant_created:
            print(f"  ✓ Created variant: {color.name} - Size {size_val}")
            
            # Add stock
            Stock.objects.get_or_create(
                variant=variant,
                store=store,
                defaults={'quantity': 10}
            )
    
    # Add product image
    img, img_created = ProductImage.objects.get_or_create(
        product=product,
        color=color,
        defaults={
            'image': color_info['image'],
            'is_primary': color_info == color_data[0]
        }
    )
    
    if img_created:
        print(f"  ✓ Added image for {color.name}")

print(f"\n✅ Product B600 successfully added with {len(color_data)} colors and {len(size_values)} sizes!")
print(f"Total variants created: {len(color_data) * len(size_values)}")
