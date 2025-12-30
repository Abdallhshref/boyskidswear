from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import ProductVariant
from .models import OrderItem, Order
from .cart import Cart
from .forms import OrderCreateForm, OrderTrackingForm

@require_POST
def cart_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    # Simple add logic, assuming qty 1 for now unless form provides it
    cart.add(variant=variant, quantity=1)
    return redirect('cart_detail')

def cart_remove(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('home')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    variant=item['variant'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                
            # Deduct Stock
                # Note: This is a simple implementation. In production, use F() expressions and atomic transactions
                variant = item['variant']
                stock = variant.stocks.first() # Simplifying: taking from first available store
                if stock:
                    stock.quantity -= item['quantity']
                    stock.save()

            # --- PAYMOB INTEGRATION START ---
            # 1. Authenticate with Paymob API
            # 2. Register Order
            # 3. Request Payment Key
            # 4. Redirect user to Paymob IFrame: https://accept.paymob.com/api/acceptance/iframes/{{iframe_id}}?payment_token={{token}}
            # 
            # For now, we simulate a successful payment locally.
            order.is_paid = True # Mark as paid for demo (or set 'pending' if waiting for callback)
            order.save()
            # --- PAYMOB INTEGRATION END ---

            cart.clear()
            # Send invoice / redirect to success
            return redirect('order_created', order_id=order.tracking_id)
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

def order_created(request, order_id):
    order = get_object_or_404(Order, tracking_id=order_id)
    return render(request, 'orders/created.html', {'order': order})

def track_order(request):
    order = None
    form = OrderTrackingForm(request.GET or None)
    
    if form.is_valid():
        tracking_id = form.cleaned_data['tracking_id']
        try:
            order = Order.objects.get(tracking_id=tracking_id)
        except Order.DoesNotExist:
            form.add_error('tracking_id', "Order not found")

    return render(request, 'orders/track_order.html', {'form': form, 'order': order})

def download_invoice(request, order_id):
    # Placeholder for invoice download
    return redirect('order_created', order_id=order_id)

def resend_invoice(request, order_id):
    # Placeholder for resending invoice
    return redirect('order_created', order_id=order_id)
