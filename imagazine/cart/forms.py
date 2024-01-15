from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CatrAddForm(forms.Form):
    count = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)