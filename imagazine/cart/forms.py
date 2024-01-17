from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CatrAddForm(forms.Form):
    count = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, initial=1, label='', required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        for key, value in cleaned_data.items():
            if key == 'count' and type(value) != int:
                cleaned_data[key] = self.initial[key]
        return cleaned_data