from django import forms

class CouponForm(forms.Form):
    coupon = forms.CharField(required=False, max_length=50, label='Промокод', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 15%;'}))