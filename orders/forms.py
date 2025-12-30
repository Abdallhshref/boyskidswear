from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'iphone_number', 'address', 'city']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'iphone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Shipping Address', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
        }

from django.utils.translation import gettext_lazy as _

class OrderTrackingForm(forms.Form):
    tracking_id = forms.UUIDField(label=_("Tracking ID"), widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('Enter your Order ID')}))
