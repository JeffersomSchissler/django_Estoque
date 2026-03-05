from django import forms
from .models import Produto, Categoria  # assumindo que você tem o modelo Categoria

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['name', 'description', 'unit_price', 'category', 'sku', 'Inventory_quantity']