
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Product

products = Product.objects.all().order_by('slug')
print(f"{'Product':<40} | {'Category':<20}")
print("-" * 65)
for p in products:
    cat_name = p.category.name if p.category else "No Category"
    print(f"{p.slug:<40} | {cat_name:<20}")
