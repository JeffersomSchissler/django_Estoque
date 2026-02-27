from django.db import models
from django.db.models import PROTECT
from django.contrib.auth import get_user_model

User = get_user_model()


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=200, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Categoria, on_delete=PROTECT)
    creation_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Fornecedor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)  
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MovimentoEstoque(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Produto, on_delete=PROTECT)
    
    class MovementType(models.TextChoices):
        INCOMING = 'I', 'Incoming'
        OUTGOING = 'O', 'Outgoing'

    movement_type = models.CharField(
        max_length=1,
        choices=MovementType.choices,
        default=MovementType.INCOMING,
        verbose_name='Movement Type'
    )
    
    amount = models.IntegerField()
    movement_date = models.DateField(auto_now_add=True)
    responsible_user = models.ForeignKey(User, on_delete=PROTECT)

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} - {self.amount}"