from django import forms
from .models import ProdMast,StckMain,StckDetail

class ProdForm(forms.ModelForm):
    class Meta:
        model = ProdMast
        fields = ['prod_name', 'sku', 'unit_price']
        widgets = {
            'prod_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name.strip()) < 2:
            raise forms.ValidationError("Product name must be at least 2 characters.")
        return name

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            raise forms.ValidationError("SKU is required.")
        if ProdMast.objects.filter(sku=sku).exists():
            raise forms.ValidationError("SKU already exists.")
        return sku

    def clean_unit_price(self):
        price = self.cleaned_data.get('unit_price')
        if price is None or price <= 0:
            raise forms.ValidationError("Unit price must be greater than 0.")
        return price
    
    
class StckMainForm(forms.ModelForm):
    class Meta:
        model = StckMain
        fields = ['transaction_type', 'reference_number', 'notes']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class StckDetailForm(forms.ModelForm):
    class Meta:
        model = StckDetail
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        
