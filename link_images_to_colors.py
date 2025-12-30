"""
Script to link existing product images to colors based on filename patterns
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product, ProductImage, Color

# Define color mappings by product and filename patterns
mappings = {
    'B604': {
        'pink': 'Pink & Black',
        'white': 'White & Black',
        'blue': 'Sky Blue & Black',
    },
    'B605': {
        'lavender': 'Lavender & Mauve',
        'skyblue': 'Sky Blue & Hot Pink',
        'peach': 'Peach & Turquoise',
    },
    'B606': {
        'navy': 'Navy & White',
        'red': 'Red & White',
        'mauve': 'Mauve & White',
    }
}

for product_code, color_map in mappings.items():
    try:
        product = Product.objects.get(slug__icontains=product_code.lower())
        print(f"\nProcessing {product.name}...")
        
        for img in product.images.all():
            filename = os.path.basename(img.image.name).lower()
            for pattern, color_name in color_map.items():
                if pattern in filename:
                    try:
                        color = Color.objects.get(name=color_name)
                        img.color = color
                        img.save()
                        print(f"  [OK] Linked {filename} to {color_name}")
                    except Color.DoesNotExist:
                        print(f"  [WARN] Color '{color_name}' not found")
                    break
    except Product.DoesNotExist:
        print(f"Product {product_code} not found")

print("\n[DONE] Image-color linking complete!")
