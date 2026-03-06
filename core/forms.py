from django import forms
from .models import Produto, Categoria

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['name', 'description', 'unit_price', 'category', 'sku', 'Inventory_quantity']

class CategoryForms(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['name', 'description']